"""
Buckshot Roulette - Logica del juego (Semana 1).

Este modulo contiene UNICAMENTE la logica del juego, sin ninguna interfaz.
Esa separacion es intencional: las pruebas unitarias prueban estas clases
directamente, y mas adelante la interfaz (consola con rich o GUI con tkinter)
se construira ENCIMA de esta logica sin modificarla.

Clases principales:
    - TipoBala : enum con los dos tipos de cartucho (REAL, FOGUEO).
    - Jugador  : un jugador con puntos de vida (HP).
    - Escopeta : la recamara con las balas mezcladas.
    - Juego    : orquesta jugadores, escopeta, turnos y condicion de victoria.
"""

import random
from enum import Enum


class TipoBala(Enum):
    """Los dos tipos de cartucho que puede tener la escopeta."""
    REAL = "real"      # quita 1 de HP
    FOGUEO = "fogueo"  # no hace dano


class Jugador:
    """Representa a un jugador con un nombre y puntos de vida (HP)."""

    def __init__(self, nombre, hp_maximo=3):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self.hp = hp_maximo

    def recibir_dano(self, cantidad=1):
        """Resta HP al jugador. El HP nunca baja de 0."""
        self.hp = max(0, self.hp - cantidad)

    def curar(self, cantidad=1):
        """Suma HP al jugador. El HP nunca supera el maximo."""
        self.hp = min(self.hp_maximo, self.hp + cantidad)

    def esta_vivo(self):
        """Devuelve True si al jugador le queda al menos 1 de HP."""
        return self.hp > 0

    def __repr__(self):
        return f"Jugador({self.nombre!r}, hp={self.hp}/{self.hp_maximo})"


class Escopeta:
    """La escopeta y su recamara de balas.

    Internamente la recamara es una lista de TipoBala.
    El frente de la escopeta (la proxima bala a salir) es el indice 0.
    """

    def __init__(self):
        self.recamara = []

    def cargar(self, num_reales, num_fogueo):
        """Carga la recamara con balas reales y de fogueo, luego las mezcla."""
        balas = [TipoBala.REAL] * num_reales + [TipoBala.FOGUEO] * num_fogueo
        random.shuffle(balas)
        self.recamara = balas

    def esta_vacia(self):
        """Devuelve True si no quedan balas en la recamara."""
        return len(self.recamara) == 0

    def balas_restantes(self):
        """Numero de balas que quedan en la recamara."""
        return len(self.recamara)

    def disparar(self):
        """Saca y devuelve la bala del frente. Error si esta vacia."""
        if self.esta_vacia():
            raise ValueError("No se puede disparar: la recamara esta vacia.")
        return self.recamara.pop(0)

    def espiar(self):
        """Revela el tipo de la proxima bala SIN sacarla (usado por la Lupa)."""
        if self.esta_vacia():
            raise ValueError("No se puede espiar: la recamara esta vacia.")
        return self.recamara[0]

    def __repr__(self):
        return f"Escopeta(balas_restantes={self.balas_restantes()})"


class Juego:
    """Orquesta la partida entre dos jugadores.

    Gestiona los turnos, los disparos y la condicion de victoria.
    El jugador actual se identifica con el indice self.turno (0 o 1).
    """

    OBJETIVOS_VALIDOS = ("yo", "oponente")

    def __init__(self, nombre1, nombre2, hp=3):
        self.jugadores = [Jugador(nombre1, hp), Jugador(nombre2, hp)]
        self.escopeta = Escopeta()
        self.turno = 0  # indice del jugador al que le toca

    def jugador_actual(self):
        """Devuelve el jugador al que le toca jugar."""
        return self.jugadores[self.turno]

    def oponente(self):
        """Devuelve el jugador que NO esta jugando este turno."""
        return self.jugadores[1 - self.turno]

    def cambiar_turno(self):
        """Pasa el turno al otro jugador."""
        self.turno = 1 - self.turno

    def disparar(self, objetivo):
        """Dispara la escopeta a 'yo' o a 'oponente'.

        Reglas:
            - Bala REAL: quita 1 de HP al blanco.
            - Bala FOGUEO: no hace dano.
            - Dispararse a si mismo con FOGUEO conserva el turno.
            - Cualquier otro caso pasa el turno al oponente.

        Devuelve el TipoBala que salio, para que la interfaz lo muestre.
        """
        if objetivo not in self.OBJETIVOS_VALIDOS:
            raise ValueError(
                f"Objetivo invalido: {objetivo!r}. "
                f"Usa uno de {self.OBJETIVOS_VALIDOS}."
            )

        bala = self.escopeta.disparar()
        blanco = self.jugador_actual() if objetivo == "yo" else self.oponente()

        if bala == TipoBala.REAL:
            blanco.recibir_dano(1)

        # El unico caso que conserva el turno: dispararse fogueo a uno mismo.
        conserva_turno = (objetivo == "yo" and bala == TipoBala.FOGUEO)
        if not conserva_turno:
            self.cambiar_turno()

        return bala

    def hay_ganador(self):
        """Devuelve el jugador ganador si solo queda uno vivo, si no None."""
        vivos = [j for j in self.jugadores if j.esta_vivo()]
        if len(vivos) == 1:
            return vivos[0]
        return None
