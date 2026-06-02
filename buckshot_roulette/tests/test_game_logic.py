"""
Pruebas unitarias del juego Buckshot Roulette (Semana 1).

Filosofia TDD aplicada:
    1. Estas pruebas se escribieron ANTES de la implementacion real.
    2. Primero se ejecutaron contra un stub vacio -> TODAS fallaron (fase RED).
    3. Luego se implemento el codigo minimo en game_logic.py -> TODAS pasaron (fase GREEN).

El azar (random.shuffle) se controla con unittest.mock para que las pruebas
sean deterministas y no dependan de la suerte. Asi sabemos exactamente que bala
sale en cada disparo.
"""

import unittest
from unittest.mock import patch

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_logic import Jugador, Escopeta, Juego, TipoBala


def _no_shuffle(lista):
    """Reemplaza random.shuffle por una funcion que NO mezcla.

    Asi la recamara conserva el orden con que fue construida:
    primero todas las balas REALES y luego todas las de FOGUEO.
    Esto nos permite predecir el resultado de cada disparo.
    """
    return None


class TestEscopeta(unittest.TestCase):

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_escopeta_carga_balas_correctas(self):
        """La recamara debe contener exactamente las balas que se cargaron."""
        escopeta = Escopeta()
        escopeta.cargar(num_reales=2, num_fogueo=3)
        self.assertEqual(escopeta.balas_restantes(), 5)

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_recamara_vacia_detectada(self):
        """Una escopeta sin cargar debe reportarse como vacia."""
        escopeta = Escopeta()
        self.assertTrue(escopeta.esta_vacia())

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_disparar_escopeta_vacia_lanza_error(self):
        """Disparar sin balas debe lanzar un error controlado."""
        escopeta = Escopeta()
        with self.assertRaises(ValueError):
            escopeta.disparar()

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_espiar_no_consume_bala(self):
        """Espiar (lupa) revela la proxima bala SIN sacarla de la recamara."""
        escopeta = Escopeta()
        escopeta.cargar(num_reales=1, num_fogueo=1)
        antes = escopeta.balas_restantes()
        bala_espiada = escopeta.espiar()
        despues = escopeta.balas_restantes()
        self.assertEqual(antes, despues)
        self.assertEqual(bala_espiada, TipoBala.REAL)


class TestJugador(unittest.TestCase):

    def test_jugador_inicia_con_hp_maximo(self):
        """Un jugador nuevo debe iniciar con su HP al maximo."""
        jugador = Jugador("Ana", hp_maximo=3)
        self.assertEqual(jugador.hp, 3)
        self.assertTrue(jugador.esta_vivo())

    def test_recibir_dano_reduce_hp(self):
        """Recibir dano debe restar HP al jugador."""
        jugador = Jugador("Ana", hp_maximo=3)
        jugador.recibir_dano(1)
        self.assertEqual(jugador.hp, 2)

    def test_jugador_muere_con_hp_cero(self):
        """Cuando el HP llega a 0 el jugador deja de estar vivo."""
        jugador = Jugador("Ana", hp_maximo=2)
        jugador.recibir_dano(2)
        self.assertEqual(jugador.hp, 0)
        self.assertFalse(jugador.esta_vivo())

    def test_hp_no_supera_maximo_al_curar(self):
        """Curar nunca debe dejar al jugador por encima de su HP maximo."""
        jugador = Jugador("Ana", hp_maximo=3)
        jugador.curar(5)
        self.assertEqual(jugador.hp, 3)


class TestJuego(unittest.TestCase):

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_disparo_bala_real_reduce_hp(self):
        """Disparar una bala REAL al oponente le quita 1 de HP."""
        juego = Juego("Ana", "Beto", hp=3)
        # Sin mezclar: la primera bala es REAL.
        juego.escopeta.cargar(num_reales=1, num_fogueo=1)
        hp_antes = juego.oponente().hp
        bala = juego.disparar("oponente")
        self.assertEqual(bala, TipoBala.REAL)
        self.assertEqual(juego.jugadores[1].hp, hp_antes - 1)

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_disparo_fogueo_no_reduce_hp(self):
        """Disparar una bala de FOGUEO no quita HP a nadie."""
        juego = Juego("Ana", "Beto", hp=3)
        # Cargamos solo fogueo: la primera bala es FOGUEO.
        juego.escopeta.cargar(num_reales=0, num_fogueo=2)
        hp_antes = juego.oponente().hp
        bala = juego.disparar("oponente")
        self.assertEqual(bala, TipoBala.FOGUEO)
        self.assertEqual(juego.jugadores[1].hp, hp_antes)

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_turno_alterna_al_disparar_al_oponente(self):
        """Tras disparar al oponente el turno pasa al otro jugador."""
        juego = Juego("Ana", "Beto", hp=3)
        juego.escopeta.cargar(num_reales=2, num_fogueo=0)
        self.assertEqual(juego.jugador_actual().nombre, "Ana")
        juego.disparar("oponente")
        self.assertEqual(juego.jugador_actual().nombre, "Beto")

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_fogueo_a_si_mismo_mantiene_turno(self):
        """Dispararse a si mismo con FOGUEO conserva el turno (regla clasica)."""
        juego = Juego("Ana", "Beto", hp=3)
        juego.escopeta.cargar(num_reales=0, num_fogueo=2)
        juego.disparar("yo")
        self.assertEqual(juego.jugador_actual().nombre, "Ana")

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_objetivo_invalido_lanza_error(self):
        """Un objetivo distinto de 'yo' u 'oponente' debe ser rechazado."""
        juego = Juego("Ana", "Beto", hp=3)
        juego.escopeta.cargar(num_reales=1, num_fogueo=0)
        with self.assertRaises(ValueError):
            juego.disparar("el_techo")

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_hay_ganador_cuando_oponente_muere(self):
        """Cuando un jugador queda sin HP, el otro es declarado ganador."""
        juego = Juego("Ana", "Beto", hp=1)
        juego.escopeta.cargar(num_reales=1, num_fogueo=0)
        self.assertIsNone(juego.hay_ganador())
        juego.disparar("oponente")
        ganador = juego.hay_ganador()
        self.assertIsNotNone(ganador)
        self.assertEqual(ganador.nombre, "Ana")


if __name__ == "__main__":
    unittest.main(verbosity=2)
