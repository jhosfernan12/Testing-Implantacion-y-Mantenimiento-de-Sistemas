# -*- coding: utf-8 -*-
"""
Buckshot Roulette - Interfaz por consola (Semana 2).

Usa la libreria 'rich' para dibujar el estado del juego con colores, paneles y
tablas. NO contiene logica del juego: todo lo importante (turnos, disparos,
items, puntaje, finalizacion) vive en game_logic.py. Esta capa solo lee el
estado y pide acciones al usuario, de modo que en la Semana 3 se pueda cambiar
por una interfaz grafica sin tocar la logica.

Ejecutar con:
    python3 interface_console.py
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

from game_logic import Juego, TipoBala, TipoItem, JugadaInvalida


console = Console()

# Nombre legible y descripcion de cada item.
ITEM_INFO = {
    TipoItem.LUPA:     ("Lupa",     "revela la proxima bala"),
    TipoItem.CERVEZA:  ("Cerveza",  "expulsa la bala del frente"),
    TipoItem.PASTILLA: ("Pastilla", "recupera 1 HP"),
    TipoItem.SEGUETA:  ("Segueta",  "el proximo disparo hace DOBLE daño"),
}


def panel_jugador(jugador, es_actual):
    """Construye el panel visual de un jugador (HP + inventario)."""
    corazones = Text()
    for i in range(jugador.hp_maximo):
        if i < jugador.hp:
            corazones.append("# ", style="bold red")
        else:
            corazones.append("- ", style="grey37")

    cuerpo = Text()
    cuerpo.append("HP: ")
    cuerpo.append_text(corazones)
    cuerpo.append(f" ({jugador.hp}/{jugador.hp_maximo})\n", style="dim")

    if jugador.inventario:
        cuerpo.append("Items: ", style="bold")
        nombres = [ITEM_INFO[i][0] for i in jugador.inventario]
        cuerpo.append(", ".join(nombres), style="cyan")
    else:
        cuerpo.append("Items: (ninguno)", style="dim")

    borde = "bright_yellow" if es_actual else "grey42"
    titulo = f"> {jugador.nombre} <" if es_actual else jugador.nombre
    return Panel(cuerpo, title=titulo, border_style=borde, box=box.ROUNDED, width=36)


def mostrar_estado(juego):
    """Dibuja el tablero completo: titulo, jugadores, recamara y puntaje."""
    console.rule("[bold red]BUCKSHOT ROULETTE[/bold red]")

    tabla = Table.grid(padding=1)
    tabla.add_column()
    tabla.add_column()
    tabla.add_row(
        panel_jugador(juego.jugadores[0], juego.turno == 0),
        panel_jugador(juego.jugadores[1], juego.turno == 1),
    )
    console.print(Align.center(tabla))

    recamara = Text()
    recamara.append(f"Recamara: {juego.escopeta.balas_restantes()} cartuchos  ", style="bold")
    recamara.append("[ ? ] " * juego.escopeta.balas_restantes(), style="grey58")
    console.print(Align.center(recamara))

    # Aviso de doble daño si la Segueta esta activa.
    if juego.segueta_activa:
        console.print(Align.center(
            Text("** SEGUETA ACTIVA: el proximo disparo hara DOBLE DAÑO **",
                 style="bold red")
        ))

    marcador = Text()
    marcador.append(f"Puntaje  {juego.jugadores[0].nombre}: {juego.puntaje[0]}", style="green")
    marcador.append("   |   ")
    marcador.append(f"{juego.jugadores[1].nombre}: {juego.puntaje[1]}", style="green")
    marcador.append(f"   (al mejor de {juego.asaltos_para_ganar})", style="dim")
    console.print(Align.center(marcador))
    console.print()


def anunciar_carga(juego, reales, fogueo):
    """Anuncia al inicio de la ronda cuantos cartuchos se cargaron.

    Como en el juego real: muestra los totales (reales en rojo, fogueo en azul)
    pero NO el orden, que permanece oculto.
    """
    total = reales + fogueo
    aviso = Text()
    aviso.append(f"  {total} CARTUCHOS  ", style="bold white on grey23")
    aviso.append("  ")
    aviso.append(f"{reales} REALES", style="bold red")
    aviso.append("  -  ")
    aviso.append(f"{fogueo} FOGUEO", style="bold blue")
    console.print(Align.center(Panel(aviso, border_style="grey50", box=box.HEAVY, title="Nueva ronda")))
    console.print()


def anunciar_items_entregados(juego, entregados):
    """Informa que items recibio cada jugador al inicio de la ronda.

    'entregados' es la lista [items_j0, items_j1] que devuelve iniciar_ronda.
    Si en esta ronda no se reparten items (ronda 1), se avisa de ello.
    """
    hubo_items = any(entregados)
    if not hubo_items:
        console.print(Align.center(
            Text("Esta ronda NO se reparten items.", style="italic grey58")
        ))
        console.print()
        return

    tabla = Table(title="Items entregados esta ronda", box=box.SIMPLE, title_style="bold cyan")
    tabla.add_column("Jugador", style="bold")
    tabla.add_column("Recibio")
    for jugador, recibidos in zip(juego.jugadores, entregados):
        if recibidos:
            nombres = ", ".join(ITEM_INFO[i][0] for i in recibidos)
        else:
            nombres = "(nada)"
        tabla.add_row(jugador.nombre, nombres)
    console.print(Align.center(tabla))
    console.print()


def asegurar_recamara(juego):
    """Recarga la escopeta si quedo vacia y anuncia la nueva ronda y los items.

    Se llama tanto al inicio del turno como DESPUES de usar items, porque la
    Cerveza puede vaciar la recamara a mitad del turno. Asi nunca se intenta
    disparar con la recamara vacia.

    Devuelve True si hubo recarga, False si no hizo falta.
    """
    if juego.escopeta.esta_vacia():
        reales, fogueo, entregados = juego.iniciar_ronda()
        anunciar_carga(juego, reales, fogueo)
        anunciar_items_entregados(juego, entregados)
        return True
    return False


def menu_items(juego):
    """Permite usar items antes de disparar. Redibuja el tablero al curar/segueta."""
    while True:
        actual = juego.jugador_actual()
        if not actual.inventario:
            return
        console.print("Items disponibles:", style="bold cyan")
        for idx, item in enumerate(actual.inventario, start=1):
            nombre, desc = ITEM_INFO[item]
            console.print(f"  [{idx}] {nombre} - {desc}")
        console.print("  [0] No usar items / continuar")
        eleccion = console.input("Elige un item: ").strip()

        if eleccion == "0":
            return
        if not eleccion.isdigit() or not (1 <= int(eleccion) <= len(actual.inventario)):
            console.print("Opcion invalida.", style="red")
            continue

        item = actual.inventario[int(eleccion) - 1]
        try:
            resultado = juego.usar_item(item)
        except JugadaInvalida as e:
            console.print(f"Jugada invalida: {e}", style="bold red")
            continue

        nombre = ITEM_INFO[item][0]
        if item == TipoItem.LUPA:
            color = "red" if resultado == TipoBala.REAL else "blue"
            console.print(f"La Lupa revela: la proxima bala es [{color}]{resultado.value.upper()}[/{color}].")
        elif item == TipoItem.CERVEZA:
            console.print(f"La Cerveza expulsa un cartucho [yellow]{resultado.value.upper()}[/yellow].")
        elif item == TipoItem.PASTILLA:
            # Redibujar el tablero para que se vea la curacion.
            console.print(f"[green]{actual.nombre} usa la Pastilla y recupera 1 HP.[/green]")
            mostrar_estado(juego)
        elif item == TipoItem.SEGUETA:
            # Redibujar y avisar en rojo que el proximo disparo hara doble daño.
            console.print("[bold red]Segueta acoplada. El PROXIMO disparo hara DOBLE DAÑO[/bold red] "
                          "[red](si la bala es real; si es fogueo, el item se gasta igual).[/red]")
            mostrar_estado(juego)


def turno_de_disparo(juego):
    """Pide y ejecuta la accion de disparo del jugador actual."""
    actual = juego.jugador_actual()
    while True:
        console.print(f"[bold yellow]{actual.nombre}[/bold yellow], elige tu disparo:")
        console.print("  [1] Disparar al OPONENTE")
        console.print("  [2] Dispararte a TI MISMO")
        eleccion = console.input("Accion: ").strip()
        if eleccion == "1":
            objetivo = "oponente"
            break
        if eleccion == "2":
            objetivo = "yo"
            break
        console.print("Opcion invalida.", style="red")

    tenia_segueta = juego.segueta_activa
    bala = juego.disparar(objetivo)
    quien = "a si mismo" if objetivo == "yo" else "al oponente"

    if bala == TipoBala.REAL:
        if tenia_segueta:
            texto = Text(f"BANG!  CARTUCHO REAL  +  SEGUETA\nDOBLE DAÑO: 2 HP de daño ({quien})",
                         style="bold white", justify="center")
        else:
            texto = Text(f"BANG!  CARTUCHO REAL\n1 HP de daño ({quien})",
                         style="bold white", justify="center")
        console.print(Align.center(
            Panel(texto, border_style="bold red", style="on red", box=box.DOUBLE, width=50)
        ))
    else:
        if tenia_segueta:
            texto = Text("*click*  CARTUCHO DE FOGUEO\nSin daño. La Segueta se gasto sin efecto.",
                         style="bold white", justify="center")
        else:
            texto = Text(f"*click*  CARTUCHO DE FOGUEO\nSin daño ({quien})",
                         style="bold white", justify="center")
        console.print(Align.center(
            Panel(texto, border_style="bold blue", style="on blue", box=box.DOUBLE, width=50)
        ))
    console.print()


def jugar():
    """Bucle principal del juego para dos jugadores reales en la misma PC."""
    console.rule("[bold]BIENVENIDOS A BUCKSHOT ROULETTE[/bold]")
    n1 = console.input("Nombre del Jugador 1: ").strip() or "Jugador 1"
    n2 = console.input("Nombre del Jugador 2: ").strip() or "Jugador 2"
    juego = Juego(n1, n2, hp=3, asaltos_para_ganar=2)

    while not juego.esta_terminado():
        # 1) Asegurar que haya balas al inicio del turno.
        asegurar_recamara(juego)

        mostrar_estado(juego)
        menu_items(juego)

        # 2) La Cerveza pudo haber vaciado la recamara: recargar antes de disparar.
        if juego.escopeta.esta_vacia():
            console.print("[bold]La recamara quedo vacia tras usar items. Se recarga...[/bold]")
            asegurar_recamara(juego)
            mostrar_estado(juego)

        turno_de_disparo(juego)

        if juego.hay_ganador() is not None:
            perdedor = juego.oponente() if juego.jugador_actual() is juego.hay_ganador() else juego.jugador_actual()
            ganador_asalto = juego.finalizar_asalto()
            console.print(Align.center(Panel(
                Text(f"{ganador_asalto.nombre} GANA EL ASALTO\nMarcador  "
                     f"{juego.jugadores[0].nombre} {juego.puntaje[0]} - "
                     f"{juego.puntaje[1]} {juego.jugadores[1].nombre}",
                     style="bold white", justify="center"),
                border_style="bold green", style="on green", box=box.DOUBLE, width=50
            )))
            if not juego.esta_terminado():
                console.print("[italic]Se reinicia todo (HP, items y cartuchos) para el siguiente asalto.[/italic]")
                console.input("Presiona Enter para el siguiente asalto...")

    campeon = juego.ganador_partida()
    console.rule("[bold green]FIN DE LA PARTIDA[/bold green]")
    console.print(Align.center(f"[bold green]CAMPEON: {campeon.nombre}[/bold green]"))
    console.print(Align.center(f"Marcador final  {juego.jugadores[0].nombre} {juego.puntaje[0]} - {juego.puntaje[1]} {juego.jugadores[1].nombre}"))


if __name__ == "__main__":
    try:
        jugar()
    except KeyboardInterrupt:
        console.print("\nJuego interrumpido. Hasta la proxima!")
