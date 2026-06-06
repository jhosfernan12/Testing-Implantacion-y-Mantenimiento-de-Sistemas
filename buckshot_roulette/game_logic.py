"""
Buckshot Roulette - Logica del juego (Semanas 1 y 2).

Este modulo contiene UNICAMENTE la logica del juego, sin ninguna interfaz.
La interfaz por consola (rich) y la grafica (tkinter) se construyen ENCIMA de
estas clases sin modificarlas. Asi las pruebas unitarias corren sin abrir
ninguna ventana ni pedir input.

Contenido:
    SEMANA 1 (logica base)
        - TipoBala : enum de cartuchos (REAL, FOGUEO).
        - Jugador  : jugador con HP.
        - Escopeta : recamara con balas mezcladas.
        - Juego    : turnos, disparos y condicion de victoria.

    SEMANA 2 (logica principal)
        - TipoItem      : enum de items (LUPA, CERVEZA, PASTILLA, SEGUETA).
        - EstadoJuego   : enum de estados (EN_CURSO, TERMINADO).
        - JugadaInvalida: excepcion propia para el control de errores.
        - Inventario de items en Jugador.
        - Carga aleatoria de la escopeta (2 a 8 cartuchos por ronda).
        - Reparto de items, uso de items, puntaje, estados y finalizacion.
"""

import random
from enum import Enum


# ======================================================================
# ENUMS Y EXCEPCIONES
# ======================================================================
class TipoBala(Enum):
    """Los dos tipos de cartucho que puede tener la escopeta."""
    REAL = "real"      # quita HP
    FOGUEO = "fogueo"  # no hace dano


class TipoItem(Enum):
    """Items que un jugador puede recibir y usar (Semana 2)."""
    LUPA = "lupa"          # revela la proxima bala sin consumirla
    CERVEZA = "cerveza"    # expulsa la bala del frente sin disparar
    PASTILLA = "pastilla"  # recupera 1 HP
    SEGUETA = "segueta"    # el proximo disparo hace doble dano


class EstadoJuego(Enum):
    """Estados posibles de la partida."""
    EN_CURSO = "en_curso"
    TERMINADO = "terminado"


class JugadaInvalida(ValueError):
    """Se lanza cuando un jugador intenta una accion no permitida.

    Centraliza el control de errores del juego: usar un item que no se tiene,
    curarse con el HP lleno, finalizar un asalto sin ganador, etc.

    Hereda de ValueError para mantener compatibilidad con las pruebas de la
    Semana 1, que esperaban un ValueError ante un objetivo de disparo invalido.
    """
    pass


# ======================================================================
# JUGADOR
# ======================================================================
class Jugador:
    """Jugador con nombre, puntos de vida (HP) e inventario de items."""

    INVENTARIO_MAXIMO = 4  # RF-17: tope de items por jugador

    def __init__(self, nombre, hp_maximo=3):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self.hp = hp_maximo
        self.inventario = []

    # ---- HP ----------------------------------------------------------
    def recibir_dano(self, cantidad=1):
        """Resta HP al jugador. El HP nunca baja de 0."""
        self.hp = max(0, self.hp - cantidad)

    def curar(self, cantidad=1):
        """Suma HP al jugador. El HP nunca supera el maximo."""
        self.hp = min(self.hp_maximo, self.hp + cantidad)

    def esta_vivo(self):
        """Devuelve True si al jugador le queda al menos 1 de HP."""
        return self.hp > 0

    def esta_a_full_hp(self):
        """Devuelve True si el jugador tiene el HP al maximo."""
        return self.hp >= self.hp_maximo

    # ---- Inventario --------------------------------------------------
    def agregar_item(self, item):
        """Agrega un item al inventario respetando el tope (RF-17).

        Devuelve True si se agrego, False si el inventario estaba lleno.
        """
        if len(self.inventario) >= self.INVENTARIO_MAXIMO:
            return False
        self.inventario.append(item)
        return True

    def tiene_item(self, item):
        """Devuelve True si el jugador posee al menos una unidad del item."""
        return item in self.inventario

    def quitar_item(self, item):
        """Quita una unidad del item. Lanza JugadaInvalida si no lo tiene."""
        if not self.tiene_item(item):
            raise JugadaInvalida(
                f"{self.nombre} no posee el item {item.value}."
            )
        self.inventario.remove(item)

    def vaciar_inventario(self):
        """Elimina todos los items (se usa al iniciar un nuevo asalto)."""
        self.inventario = []

    def __repr__(self):
        return f"Jugador({self.nombre!r}, hp={self.hp}/{self.hp_maximo})"


# ======================================================================
# ESCOPETA
# ======================================================================
class Escopeta:
    """La escopeta y su recamara. El frente (proxima bala) es el indice 0."""

    CARTUCHOS_MIN = 2
    CARTUCHOS_MAX = 8

    def __init__(self):
        self.recamara = []
        # Totales de la ultima carga (se muestran al inicio de la ronda).
        self.ultima_carga = {"reales": 0, "fogueo": 0, "total": 0}

    def cargar(self, num_reales, num_fogueo):
        """Carga la recamara con balas reales y de fogueo, luego las mezcla."""
        balas = [TipoBala.REAL] * num_reales + [TipoBala.FOGUEO] * num_fogueo
        random.shuffle(balas)
        self.recamara = balas
        self.ultima_carga = {
            "reales": num_reales,
            "fogueo": num_fogueo,
            "total": num_reales + num_fogueo,
        }

    def cargar_aleatoria(self):
        """Carga entre 2 y 8 cartuchos con reparto reales/fogueo aleatorio.

        Garantiza al menos 1 bala real y 1 de fogueo, como en el juego real.
        Devuelve la tupla (num_reales, num_fogueo).
        """
        total = random.randint(self.CARTUCHOS_MIN, self.CARTUCHOS_MAX)
        num_reales = random.randint(1, total - 1)  # entre 1 y total-1
        num_fogueo = total - num_reales
        self.cargar(num_reales, num_fogueo)
        return (num_reales, num_fogueo)

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


# ======================================================================
# JUEGO
# ======================================================================
class Juego:
    """Orquesta la partida entre dos jugadores.

    Gestiona turnos, disparos, items, puntaje, estados y la condicion de
    finalizacion. El jugador actual se identifica con el indice self.turno.

    Conceptos:
        - asalto : se juega hasta que un jugador llega a 0 HP. El ganador
                   del asalto suma un punto.
        - partida: se gana al alcanzar 'asaltos_para_ganar' puntos.
        - ronda  : una recarga de la escopeta; al iniciar una ronda se
                   reparten items y se cargan entre 2 y 8 cartuchos al azar.
    """

    OBJETIVOS_VALIDOS = ("yo", "oponente")
    ITEMS_DISPONIBLES = (
        TipoItem.LUPA,
        TipoItem.CERVEZA,
        TipoItem.PASTILLA,
        TipoItem.SEGUETA,
    )
    DANO_NORMAL = 1
    DANO_SEGUETA = 2

    def __init__(self, nombre1, nombre2, hp=3, asaltos_para_ganar=1):
        self.jugadores = [Jugador(nombre1, hp), Jugador(nombre2, hp)]
        self.escopeta = Escopeta()
        self.turno = 0
        self.estado = EstadoJuego.EN_CURSO
        self.puntaje = [0, 0]
        self.asaltos_para_ganar = asaltos_para_ganar
        self.ronda = 0
        self.segueta_activa = False  # doble dano para el proximo disparo

    # ---- Turnos ------------------------------------------------------
    def jugador_actual(self):
        """Devuelve el jugador al que le toca jugar."""
        return self.jugadores[self.turno]

    def oponente(self):
        """Devuelve el jugador que NO esta jugando este turno."""
        return self.jugadores[1 - self.turno]

    def _cambiar_turno(self):
        """Pasa el turno al otro jugador (metodo interno)."""
        self.turno = 1 - self.turno

    def cambiar_turno(self):
        """Alias publico mantenido por compatibilidad con la Semana 1."""
        self._cambiar_turno()

    # ---- Rondas e items ---------------------------------------------
    def iniciar_ronda(self, repartir=True):
        """Inicia una ronda: carga 2-8 cartuchos al azar y reparte items.

        Devuelve la tupla (num_reales, num_fogueo) para que la interfaz pueda
        anunciar cuantos cartuchos de cada tipo se cargaron.
        """
        reales, fogueo = self.escopeta.cargar_aleatoria()
        self.ronda += 1
        if repartir:
            self.repartir_items()
        return (reales, fogueo)

    def repartir_items(self, minimo=1, maximo=2):
        """RF-15: reparte entre 'minimo' y 'maximo' items a cada jugador.

        Los items se eligen al azar del pool ITEMS_DISPONIBLES y pueden
        repetirse. Respeta el tope de inventario de cada jugador.
        """
        for jugador in self.jugadores:
            cantidad = random.randint(minimo, maximo)
            for _ in range(cantidad):
                item = random.choice(self.ITEMS_DISPONIBLES)
                jugador.agregar_item(item)

    def usar_item(self, tipo):
        """Usa un item del jugador actual y aplica su efecto (RF-16).

        Valida que el jugador posea el item y que la jugada sea legal.
        Devuelve informacion util segun el item (la bala revelada por la Lupa
        o descartada por la Cerveza); para Pastilla/Segueta devuelve None.
        Lanza JugadaInvalida ante cualquier jugada no permitida.
        """
        actual = self.jugador_actual()
        if not actual.tiene_item(tipo):
            raise JugadaInvalida(
                f"{actual.nombre} no tiene el item {tipo.value}."
            )

        if tipo == TipoItem.LUPA:
            if self.escopeta.esta_vacia():
                raise JugadaInvalida("No hay balas para espiar con la Lupa.")
            resultado = self.escopeta.espiar()

        elif tipo == TipoItem.CERVEZA:
            if self.escopeta.esta_vacia():
                raise JugadaInvalida("No hay balas para expulsar con la Cerveza.")
            resultado = self.escopeta.disparar()  # descarta el frente, sin dano

        elif tipo == TipoItem.PASTILLA:
            if actual.esta_a_full_hp():
                raise JugadaInvalida("No se puede usar la Pastilla con el HP lleno.")
            actual.curar(1)
            resultado = None

        elif tipo == TipoItem.SEGUETA:
            if self.segueta_activa:
                raise JugadaInvalida("La Segueta ya esta activa: no se acumula.")
            self.segueta_activa = True
            resultado = None

        else:
            raise JugadaInvalida(f"Item desconocido: {tipo!r}.")

        # El item se consume solo si la jugada fue valida.
        actual.quitar_item(tipo)
        return resultado

    # ---- Disparo -----------------------------------------------------
    def disparar(self, objetivo):
        """Dispara la escopeta a 'yo' o a 'oponente'.

        Reglas:
            - Bala REAL: quita HP al blanco (2 si la Segueta esta activa, si no 1).
            - Bala FOGUEO: no hace dano.
            - Dispararse a si mismo con FOGUEO conserva el turno.
            - Cualquier otro caso pasa el turno al oponente.
            - La Segueta se consume con este disparo, salga real o fogueo.

        Devuelve el TipoBala que salio.
        """
        if objetivo not in self.OBJETIVOS_VALIDOS:
            raise JugadaInvalida(
                f"Objetivo invalido: {objetivo!r}. "
                f"Usa uno de {self.OBJETIVOS_VALIDOS}."
            )

        bala = self.escopeta.disparar()
        blanco = self.jugador_actual() if objetivo == "yo" else self.oponente()

        dano = self.DANO_SEGUETA if self.segueta_activa else self.DANO_NORMAL
        if bala == TipoBala.REAL:
            blanco.recibir_dano(dano)

        # La Segueta se gasta con el disparo, sin importar el resultado.
        self.segueta_activa = False

        conserva_turno = (objetivo == "yo" and bala == TipoBala.FOGUEO)
        if not conserva_turno:
            self._cambiar_turno()

        return bala

    # ---- Puntaje, estados y finalizacion -----------------------------
    def hay_ganador(self):
        """Devuelve el jugador vivo si solo queda uno (fin del asalto), si no None."""
        vivos = [j for j in self.jugadores if j.esta_vivo()]
        if len(vivos) == 1:
            return vivos[0]
        return None

    def finalizar_asalto(self):
        """Cierra el asalto actual: otorga el punto y decide si la partida sigue.

        Requiere que exista un ganador de asalto (un jugador en 0 HP).
        Si el ganador alcanza 'asaltos_para_ganar', la partida termina; en
        caso contrario, se reinicia el HP y el inventario de ambos.
        Devuelve el jugador que gano el asalto.
        Lanza JugadaInvalida si todavia no hay ganador.
        """
        ganador = self.hay_ganador()
        if ganador is None:
            raise JugadaInvalida("No se puede finalizar el asalto: nadie ha caido.")

        indice = self.jugadores.index(ganador)
        self.puntaje[indice] += 1

        if self.puntaje[indice] >= self.asaltos_para_ganar:
            self.estado = EstadoJuego.TERMINADO
        else:
            for jugador in self.jugadores:
                jugador.hp = jugador.hp_maximo
                jugador.vaciar_inventario()
            self.turno = 0
            self.segueta_activa = False

        return ganador

    def ganador_partida(self):
        """Devuelve el jugador que gano la partida, o None si sigue en curso."""
        for indice, puntos in enumerate(self.puntaje):
            if puntos >= self.asaltos_para_ganar:
                return self.jugadores[indice]
        return None

    def esta_terminado(self):
        """Devuelve True si la partida ya termino."""
        return self.estado == EstadoJuego.TERMINADO