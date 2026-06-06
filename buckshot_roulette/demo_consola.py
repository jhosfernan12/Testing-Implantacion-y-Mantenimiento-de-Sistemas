"""
Demo automatica de Buckshot Roulette por consola (Semana 2).
"""

from unittest.mock import patch

from rich.console import Console
from rich.text import Text

from game_logic import Juego, TipoBala, TipoItem
import interface_console as ui

console = Console(record=True, width=92)
ui.console = console  # reutilizamos las funciones de dibujo de la interfaz real


def narrar(texto):
    console.print(f"[italic grey58]>> {texto}[/italic grey58]")


def demo():
    console.rule("[bold red]DEMO AUTOMATICA - BUCKSHOT ROULETTE[/bold red]")
    narrar("Partida de ejemplo entre 'Jhostyn' y 'Janitza' (al mejor de 2).")

    juego = Juego("Jhostyn", "Janitza", hp=3, asaltos_para_ganar=2)

    # --- Inicio de ronda: cargamos de forma controlada para una demo estable ---
    # (en el juego real se usa juego.iniciar_ronda(), que carga 2-8 al azar)
    juego.escopeta.cargar(num_reales=3, num_fogueo=2)  # 5 cartuchos: 3 reales, 2 fogueo
    juego.ronda += 1
    juego.jugadores[0].agregar_item(TipoItem.SEGUETA)
    juego.jugadores[0].agregar_item(TipoItem.LUPA)
    juego.jugadores[1].agregar_item(TipoItem.PASTILLA)
    ui.anunciar_carga(juego, reales=3, fogueo=2)
    ui.mostrar_estado(juego)

    # --- Jhostyn usa la Lupa y luego la Segueta (doble daño) ---
    narrar("Jhostyn usa la Lupa para espiar la proxima bala.")
    revelada = juego.usar_item(TipoItem.LUPA)
    color = "red" if revelada == TipoBala.REAL else "blue"
    console.print(f"La Lupa revela: la proxima bala es [{color}]{revelada.value.upper()}[/{color}].")

    narrar("Jhostyn acopla la Segueta: el proximo disparo hara doble daño.")
    juego.usar_item(TipoItem.SEGUETA)
    console.print("[bold red]Segueta acoplada. El PROXIMO disparo hara DOBLE DAÑO[/bold red] "
                  "[red](si es real; si es fogueo, se gasta igual).[/red]")
    ui.mostrar_estado(juego)

    # --- Jhostyn dispara al oponente con la segueta activa ---
    narrar("Jhostyn dispara a Janitza con la Segueta activa.")
    tenia = juego.segueta_activa
    bala = juego.disparar("oponente")
    if bala == TipoBala.REAL and tenia:
        console.print("[bold red]BANG! Cartucho REAL con SEGUETA: DOBLE DAÑO (-2 HP)![/bold red]")
    elif bala == TipoBala.REAL:
        console.print("[bold red]BANG! Cartucho REAL.[/bold red]")
    else:
        console.print("[blue]*click* Cartucho de FOGUEO.[/blue]")
    ui.mostrar_estado(juego)

    # --- Janitza usa la Pastilla: se redibuja el tablero y se ve la curacion ---
    narrar("Janitza esta herida y usa la Pastilla para recuperar 1 HP.")
    juego.jugadores[1].hp = max(1, juego.jugadores[1].hp)  # aseguramos que no este full
    hp_antes = juego.jugador_actual().hp if juego.turno == 1 else juego.jugadores[1].hp
    # En la demo forzamos el turno de Janitza para mostrar su curacion.
    juego.turno = 1
    if juego.jugadores[1].esta_a_full_hp():
        juego.jugadores[1].hp = 1
    juego.usar_item(TipoItem.PASTILLA)
    console.print("[green]Janitza usa la Pastilla y recupera 1 HP.[/green]")
    ui.mostrar_estado(juego)

    console.rule("[bold green]FIN DE LA DEMO[/bold green]")
    narrar("La partida continuaria hasta que alguien gane 2 asaltos.")

    console.save_svg(
        "evidencia_tdd/06_captura_consola.svg",
        title="Buckshot Roulette - Consola (rich)",
    )
    print("\n[captura guardada en evidencia_tdd/06_captura_consola.svg]")


if __name__ == "__main__":
    demo()
