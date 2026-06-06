"""
Pruebas unitarias de la logica principal - Semana 2.

Cubre los requerimientos de la Semana 2: turnos, validacion de jugadas,
puntaje, estados del juego, control de errores y condicion de finalizacion,
ademas de los items: Lupa, Cerveza, Pastilla y Segueta.

Reglas de esta version:
    - Sin Botiquin.
    - La Segueta hace que el proximo disparo haga DOBLE dano; se consume al
      disparar aunque salga fogueo.
    - Cada ronda carga entre 2 y 8 cartuchos al azar, con cantidad de reales y
      de fogueo aleatoria (al menos 1 de cada tipo).

El azar se controla con unittest.mock para que las pruebas sean deterministas.
"""

import unittest
from unittest.mock import patch

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_logic import (
    Jugador,
    Escopeta,
    Juego,
    TipoBala,
    TipoItem,
    EstadoJuego,
    JugadaInvalida,
)


def _no_shuffle(lista):
    """random.shuffle desactivado: conserva el orden de construccion."""
    return None


# ----------------------------------------------------------------------
# INVENTARIO DE ITEMS (RF-16, RF-17)
# ----------------------------------------------------------------------
class TestInventario(unittest.TestCase):

    def test_jugador_agrega_item_al_inventario(self):
        jugador = Jugador("Ana")
        jugador.agregar_item(TipoItem.LUPA)
        self.assertTrue(jugador.tiene_item(TipoItem.LUPA))

    def test_inventario_maximo_4_items(self):
        """RF-17: el inventario no debe superar los 4 items."""
        jugador = Jugador("Ana")
        for _ in range(6):
            jugador.agregar_item(TipoItem.CERVEZA)
        self.assertEqual(len(jugador.inventario), 4)

    def test_agregar_item_lleno_devuelve_false(self):
        jugador = Jugador("Ana")
        for _ in range(4):
            self.assertTrue(jugador.agregar_item(TipoItem.LUPA))
        self.assertFalse(jugador.agregar_item(TipoItem.LUPA))

    def test_items_pueden_repetirse(self):
        jugador = Jugador("Ana")
        jugador.agregar_item(TipoItem.CERVEZA)
        jugador.agregar_item(TipoItem.CERVEZA)
        self.assertEqual(jugador.inventario.count(TipoItem.CERVEZA), 2)

    def test_no_existe_botiquin(self):
        """En esta version el Botiquin fue retirado del juego."""
        nombres = [i.name for i in TipoItem]
        self.assertNotIn("BOTIQUIN", nombres)
        self.assertIn("SEGUETA", nombres)


# ----------------------------------------------------------------------
# REPARTO DE ITEMS (RF-15)
# ----------------------------------------------------------------------
class TestRepartoItems(unittest.TestCase):

    @patch("game_logic.random.randint", return_value=2)
    @patch("game_logic.random.choice", return_value=TipoItem.LUPA)
    def test_repartir_da_items_a_ambos_jugadores(self, mock_choice, mock_randint):
        juego = Juego("Ana", "Beto")
        juego.repartir_items()
        self.assertEqual(len(juego.jugadores[0].inventario), 2)
        self.assertEqual(len(juego.jugadores[1].inventario), 2)

    @patch("game_logic.random.randint", return_value=1)
    @patch("game_logic.random.choice", return_value=TipoItem.CERVEZA)
    def test_repartir_respeta_cantidad(self, mock_choice, mock_randint):
        juego = Juego("Ana", "Beto")
        juego.repartir_items()
        self.assertEqual(len(juego.jugadores[0].inventario), 1)


# ----------------------------------------------------------------------
# CARGA ALEATORIA DE LA ESCOPETA (2 a 8 cartuchos)
# ----------------------------------------------------------------------
class TestCargaAleatoria(unittest.TestCase):

    def test_total_de_cartuchos_entre_2_y_8(self):
        """La carga aleatoria siempre produce entre 2 y 8 cartuchos."""
        escopeta = Escopeta()
        for _ in range(200):
            escopeta.cargar_aleatoria()
            self.assertGreaterEqual(escopeta.balas_restantes(), 2)
            self.assertLessEqual(escopeta.balas_restantes(), 8)

    def test_siempre_al_menos_una_real_y_una_fogueo(self):
        """Cada ronda garantiza al menos una bala real y una de fogueo."""
        escopeta = Escopeta()
        for _ in range(200):
            escopeta.cargar_aleatoria()
            reales = escopeta.recamara.count(TipoBala.REAL)
            fogueo = escopeta.recamara.count(TipoBala.FOGUEO)
            self.assertGreaterEqual(reales, 1)
            self.assertGreaterEqual(fogueo, 1)

    @patch("game_logic.random.shuffle", _no_shuffle)
    @patch("game_logic.random.randint", side_effect=[6, 2])
    def test_carga_aleatoria_usa_el_azar_controlado(self, mock_randint):
        """Con azar mockeado: total=6, reales=2 -> 2 reales y 4 fogueo."""
        escopeta = Escopeta()
        escopeta.cargar_aleatoria()
        self.assertEqual(escopeta.recamara.count(TipoBala.REAL), 2)
        self.assertEqual(escopeta.recamara.count(TipoBala.FOGUEO), 4)


# ----------------------------------------------------------------------
# EFECTO DE LOS ITEMS (RF-16)
# ----------------------------------------------------------------------
class TestEfectoItems(unittest.TestCase):

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_lupa_revela_proxima_bala_sin_consumirla(self):
        juego = Juego("Ana", "Beto")
        juego.escopeta.cargar(num_reales=1, num_fogueo=1)  # frente = REAL
        juego.jugador_actual().agregar_item(TipoItem.LUPA)
        balas_antes = juego.escopeta.balas_restantes()
        revelada = juego.usar_item(TipoItem.LUPA)
        self.assertEqual(revelada, TipoBala.REAL)
        self.assertEqual(juego.escopeta.balas_restantes(), balas_antes)

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_cerveza_descarta_bala_del_frente(self):
        juego = Juego("Ana", "Beto")
        juego.escopeta.cargar(num_reales=1, num_fogueo=1)  # frente = REAL
        juego.jugador_actual().agregar_item(TipoItem.CERVEZA)
        hp_oponente_antes = juego.oponente().hp
        descartada = juego.usar_item(TipoItem.CERVEZA)
        self.assertEqual(descartada, TipoBala.REAL)
        self.assertEqual(juego.escopeta.balas_restantes(), 1)
        self.assertEqual(juego.oponente().hp, hp_oponente_antes)

    def test_pastilla_recupera_un_hp(self):
        juego = Juego("Ana", "Beto", hp=3)
        juego.jugador_actual().hp = 1
        juego.jugador_actual().agregar_item(TipoItem.PASTILLA)
        juego.usar_item(TipoItem.PASTILLA)
        self.assertEqual(juego.jugador_actual().hp, 2)

    def test_pastilla_no_supera_hp_maximo(self):
        juego = Juego("Ana", "Beto", hp=3)
        juego.jugador_actual().hp = 3
        juego.jugador_actual().agregar_item(TipoItem.PASTILLA)
        with self.assertRaises(JugadaInvalida):
            juego.usar_item(TipoItem.PASTILLA)


# ----------------------------------------------------------------------
# SEGUETA: doble dano en el proximo disparo
# ----------------------------------------------------------------------
class TestSegueta(unittest.TestCase):

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_segueta_activa_bandera(self):
        """Usar la Segueta deja la bandera de doble dano activa."""
        juego = Juego("Ana", "Beto")
        juego.escopeta.cargar(num_reales=1, num_fogueo=1)
        juego.jugador_actual().agregar_item(TipoItem.SEGUETA)
        self.assertFalse(juego.segueta_activa)
        juego.usar_item(TipoItem.SEGUETA)
        self.assertTrue(juego.segueta_activa)

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_segueta_dobla_dano_en_disparo_real(self):
        """Con la Segueta activa, una bala real quita 2 HP en vez de 1."""
        juego = Juego("Ana", "Beto", hp=3)
        juego.escopeta.cargar(num_reales=1, num_fogueo=0)  # frente = REAL
        juego.jugador_actual().agregar_item(TipoItem.SEGUETA)
        juego.usar_item(TipoItem.SEGUETA)
        juego.disparar("oponente")
        self.assertEqual(juego.jugadores[1].hp, 1)  # 3 - 2 = 1

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_segueta_se_consume_aunque_salga_fogueo(self):
        """Si tras activar la Segueta sale fogueo, el item se gasta igual."""
        juego = Juego("Ana", "Beto", hp=3)
        juego.escopeta.cargar(num_reales=0, num_fogueo=2)  # frente = FOGUEO
        juego.jugador_actual().agregar_item(TipoItem.SEGUETA)
        juego.usar_item(TipoItem.SEGUETA)
        juego.disparar("oponente")
        self.assertFalse(juego.segueta_activa)  # se gasto
        self.assertEqual(juego.jugadores[1].hp, 3)  # no hubo dano

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_segueta_no_se_acumula(self):
        """No se puede activar la Segueta dos veces seguidas."""
        juego = Juego("Ana", "Beto")
        juego.escopeta.cargar(num_reales=1, num_fogueo=1)
        juego.jugador_actual().agregar_item(TipoItem.SEGUETA)
        juego.jugador_actual().agregar_item(TipoItem.SEGUETA)
        juego.usar_item(TipoItem.SEGUETA)
        with self.assertRaises(JugadaInvalida):
            juego.usar_item(TipoItem.SEGUETA)


# ----------------------------------------------------------------------
# VALIDACION DE JUGADAS Y CONTROL DE ERRORES
# ----------------------------------------------------------------------
class TestValidacionYErrores(unittest.TestCase):

    def test_usar_item_no_poseido_lanza_error(self):
        juego = Juego("Ana", "Beto")
        with self.assertRaises(JugadaInvalida):
            juego.usar_item(TipoItem.LUPA)

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_lupa_con_recamara_vacia_lanza_error(self):
        juego = Juego("Ana", "Beto")
        juego.jugador_actual().agregar_item(TipoItem.LUPA)
        with self.assertRaises(JugadaInvalida):
            juego.usar_item(TipoItem.LUPA)

    def test_finalizar_asalto_sin_ganador_lanza_error(self):
        juego = Juego("Ana", "Beto", hp=3)
        with self.assertRaises(JugadaInvalida):
            juego.finalizar_asalto()

    def test_objetivo_invalido_lanza_error(self):
        juego = Juego("Ana", "Beto")
        juego.escopeta.cargar(num_reales=1, num_fogueo=0)
        with self.assertRaises(JugadaInvalida):
            juego.disparar("la_pared")


# ----------------------------------------------------------------------
# ESTADOS, PUNTAJE Y CONDICION DE FINALIZACION
# ----------------------------------------------------------------------
class TestEstadosYPuntaje(unittest.TestCase):

    def test_estado_inicial_es_en_curso(self):
        juego = Juego("Ana", "Beto")
        self.assertEqual(juego.estado, EstadoJuego.EN_CURSO)
        self.assertFalse(juego.esta_terminado())

    def test_puntaje_inicial_en_cero(self):
        juego = Juego("Ana", "Beto")
        self.assertEqual(juego.puntaje, [0, 0])

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_puntaje_aumenta_al_ganar_asalto(self):
        juego = Juego("Ana", "Beto", hp=1, asaltos_para_ganar=2)
        juego.escopeta.cargar(num_reales=1, num_fogueo=0)
        juego.disparar("oponente")
        juego.finalizar_asalto()
        self.assertEqual(juego.puntaje[0], 1)
        self.assertFalse(juego.esta_terminado())

    @patch("game_logic.random.shuffle", _no_shuffle)
    def test_partida_termina_al_alcanzar_asaltos(self):
        juego = Juego("Ana", "Beto", hp=1, asaltos_para_ganar=1)
        juego.escopeta.cargar(num_reales=1, num_fogueo=0)
        juego.disparar("oponente")
        juego.finalizar_asalto()
        self.assertTrue(juego.esta_terminado())
        self.assertEqual(juego.estado, EstadoJuego.TERMINADO)
        self.assertEqual(juego.ganador_partida().nombre, "Ana")

    def test_hp_se_reinicia_entre_asaltos(self):
        juego = Juego("Ana", "Beto", hp=2, asaltos_para_ganar=2)
        juego.jugadores[1].hp = 0
        juego.finalizar_asalto()
        self.assertEqual(juego.jugadores[0].hp, 2)
        self.assertEqual(juego.jugadores[1].hp, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
