# Buckshot Roulette — Práctica TDD

Juego de ruleta rusa con escopeta para **2 jugadores reales**, desarrollado en
Python aplicando la metodología **TDD (Test Driven Development)**.

> Estado actual: **Semana 1** — lógica base del juego con pruebas unitarias.
> El juego todavía no es jugable por consola; eso llega en la Semana 2.

## Estructura del proyecto

```
buckshot_roulette/
├── game_logic.py          # Lógica del juego (sin interfaz)
├── REGLAS.md              # Documento de reglas del juego
├── REQUISITOS.md          # Lista de requerimientos funcionales
├── README.md              # Este archivo
├── tests/
│   ├── __init__.py
│   └── test_game_logic.py # 14 pruebas unitarias
└── evidencia_tdd/
    ├── 01_red.txt         # Evidencia: pruebas fallando (fase RED)
    └── 02_green.txt       # Evidencia: pruebas pasando (fase GREEN)
```

## Requisitos

- Python 3.8 o superior. No se necesita instalar nada para la lógica ni las
  pruebas (usan solo la librería estándar: `unittest`, `random`, `enum`).

## Cómo ejecutar las pruebas

Desde la carpeta raíz del proyecto (`buckshot_roulette/`):

```bash
python3 -m unittest tests.test_game_logic -v
```

Resultado esperado: `Ran 14 tests ... OK`.

## Metodología TDD aplicada

El proyecto se construyó siguiendo el ciclo **Red → Green → Refactor**:

1. **Red:** se escribieron primero las 14 pruebas en `tests/test_game_logic.py`
   y se ejecutaron contra un stub vacío. Todas fallaron. Evidencia en
   `evidencia_tdd/01_red.txt`.
2. **Green:** se implementó el código mínimo en `game_logic.py` hasta que todas
   las pruebas pasaron. Evidencia en `evidencia_tdd/02_green.txt`.
3. **Refactor:** se limpió el código, se agregaron docstrings y se nombraron las
   clases y métodos de forma clara, manteniendo las pruebas en verde.

## Detalle técnico: pruebas deterministas

Como el juego usa azar (`random.shuffle` al cargar la escopeta), las pruebas
reemplazan esa función con `unittest.mock.patch` para que el orden de las balas
sea predecible. Así las pruebas siempre dan el mismo resultado y no dependen de
la suerte.

## Clases principales

- `TipoBala` — enum con los tipos de cartucho (`REAL`, `FOGUEO`).
- `Jugador` — nombre y puntos de vida; recibe daño, se cura, sabe si está vivo.
- `Escopeta` — carga, mezcla, dispara y permite espiar la próxima bala.
- `Juego` — gestiona jugadores, turnos, disparos y condición de victoria.

## Mejoras planeadas

- Semana 2: ítems (Lupa, Cerveza, Pastilla, Botiquín) + interfaz por consola con
  `rich`.
- Semana 3: ítems avanzados (Segueta, Esposas) + interfaz gráfica con `tkinter`.
