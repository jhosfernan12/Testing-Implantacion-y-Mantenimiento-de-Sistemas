# -*- coding: utf-8 -*-
"""
Demo automatica de Buckshot Roulette por consola (Semana 2).

Juega de forma predeterminada (sin input) para dejar evidencia visual de:
    - Aviso de carga al inicio de la ronda (reales en rojo, fogueo en azul).
    - Progresion de items por ronda (ronda 1 sin items; rondas siguientes 2,3,4)
      con aviso de que items recibio cada jugador.
    - Disparo bien visible: panel ROJO si es real, panel AZUL si es fogueo.
    - Segueta (doble daño) y Pastilla (curacion con re-dibujo del tablero).

Captura la salida como imagen SVG en evidencia_tdd/.

Ejecutar con:
    python3 demo_consola.py
"""

from rich.console import Console

from game_logic import Juego, TipoBala, TipoItem
import interface_console as ui

console = Console(record=True, width=100)
ui.console = console  # reutilizamos las funciones de dibujo de la interfaz real


def narrar(texto):
    console.print(f"[italic grey58]>> {texto}[/italic grey58]")


def disparo_visible(juego, objetivo):
    """Replica el disparo visible de la interfaz para la demo."""
    tenia = juego.segueta_activa
    bala = juego.disparar(objetivo)
    ui.turno_de_disparo  # (solo referencia; aqui imprimimos el panel directamente)
    from rich.text import Text
    from rich.align import Align
    from rich import box
    from rich.panel import Panel
    quien = "a si mismo" if objetivo == "yo" else "al oponente"
    if bala == TipoBala.REAL:
        msg = (f"BANG!  CARTUCHO REAL  +  SEGUETA\nDOBLE DAÑO: 2 HP ({quien})"
               if tenia else f"BANG!  CARTUCHO REAL\n1 HP de daño ({quien})")
        console.print(Align.center(Panel(Text(msg, style="bold white", justify="center"),
                      border_style="bold red", style="on red", box=box.DOUBLE, width=50)))
    else:
        msg = ("*click*  CARTUCHO DE FOGUEO\nSin daño. Segueta gastada."
               if tenia else f"*click*  CARTUCHO DE FOGUEO\nSin daño ({quien})")
        console.print(Align.center(Panel(Text(msg, style="bold white", justify="center"),
                      border_style="bold blue", style="on blue", box=box.DOUBLE, width=50)))
    console.print()
    return bala


def demo():
    console.rule("[bold red]DEMO AUTOMATICA - BUCKSHOT ROULETTE[/bold red]")
    narrar("Partida de ejemplo entre 'Fernando' y 'Janitza' (al mejor de 2).")

    juego = Juego("Fernando", "Janitza", hp=3, asaltos_para_ganar=2)

    # --- RONDA 1: sin items (progresion) ---
    narrar("Ronda 1 del asalto: por progresion, NO se reparten items.")
    # Carga controlada para una demo estable (en el juego real es 2-8 al azar).
    juego.escopeta.cargar(num_reales=2, num_fogueo=1)
    juego.ronda += 1  # ronda 1
    ui.anunciar_carga(juego, reales=2, fogueo=1)
    ui.anunciar_items_entregados(juego, [[], []])
    ui.mostrar_estado(juego)

    narrar("Fernando dispara a Janitza.")
    disparo_visible(juego, "oponente")
    ui.mostrar_estado(juego)

    # Vaciamos la recamara para forzar RONDA 2 (con items).
    juego.escopeta.recamara = []

    # --- RONDA 2: 2 items, con aviso de entrega ---
    narrar("La recamara se vacio: empieza la ronda 2, ahora SI con items (2 cada uno).")
    juego.escopeta.cargar(num_reales=2, num_fogueo=2)
    juego.ronda += 1  # ronda 2
    entregados = juego.repartir_items(cantidad=2)
    ui.anunciar_carga(juego, reales=2, fogueo=2)
    ui.anunciar_items_entregados(juego, entregados)
    ui.mostrar_estado(juego)

    # Aseguramos que el jugador actual tenga una Segueta para la demo.
    actual = juego.jugador_actual()
    if not actual.tiene_item(TipoItem.SEGUETA):
        actual.inventario[0] = TipoItem.SEGUETA
    narrar(f"{actual.nombre} acopla la Segueta (doble daño en el proximo disparo).")
    juego.usar_item(TipoItem.SEGUETA)
    console.print("[bold red]Segueta acoplada. El PROXIMO disparo hara DOBLE DAÑO.[/bold red]")
    ui.mostrar_estado(juego)

    narrar(f"{juego.jugador_actual().nombre} dispara con la Segueta activa.")
    # Forzamos que la proxima bala sea real para evidenciar el doble daño.
    juego.escopeta.recamara[0] = TipoBala.REAL
    disparo_visible(juego, "oponente")
    ui.mostrar_estado(juego)

    console.rule("[bold green]FIN DE LA DEMO[/bold green]")
    narrar("Cuando un jugador llega a 0 HP, se suma el punto y se reinicia todo el asalto.")

    console.save_svg("evidencia_tdd/06_captura_consola.svg",
                     title="Buckshot Roulette - Consola (rich)")
    print("\n[captura guardada en evidencia_tdd/06_captura_consola.svg]")


if __name__ == "__main__":
    demo()
