# Buckshot Roulette — Práctica TDD

Juego de ruleta rusa con escopeta para **2 jugadores reales**, desarrollado en
Python aplicando la metodología **TDD (Test Driven Development)**.

> Estado actual: **Semana 2 completada** — lógica principal, ítems y juego
> jugable por consola con `rich`.

## Estructura del proyecto

```
buckshot_roulette/
├── game_logic.py            # Lógica del juego (sin interfaz)
├── interface_console.py     # Interfaz jugable por consola (usa rich)
├── demo_consola.py          # Demo automática que genera la captura del juego
├── REGLAS.md                # Documento de reglas del juego
├── REQUISITOS.md            # Lista de requerimientos funcionales
├── README.md                # Este archivo
├── tests/
│   ├── __init__.py
│   ├── test_semana1.py   # 14 pruebas (Semana 1)
│   └── test_semana2[Pruebas Unitarias].py      # 21 pruebas (Semana 2)
└── evidencia_tdd/
    ├── 01_red.txt                 # S1: pruebas fallando
    ├── 02_green.txt               # S1: pruebas pasando
    ├── 03_red_semana2.txt         # S2: pruebas fallando (features no existen)
    ├── 04_green_semana2.txt       # S2: pruebas pasando
    ├── 05_suite_completa.txt      # 35 pruebas juntas pasando
    ├── 06_captura_consola.txt     # Salida de la demo por consola
    └── 06_captura_consola.svg     # Captura visual del juego (imagen)
```

## Requisitos

- Python 3.8 o superior.
- Para la **lógica y las pruebas**: nada extra (solo librería estándar).
- Para la **interfaz por consola**: `pip install rich`.

## Cómo ejecutar las pruebas

Desde la carpeta raíz del proyecto:

```bash
python3 -m unittest discover -s tests -v
```

Resultado esperado: `Ran 35 tests ... OK`.

## Cómo jugar (consola)

```bash
pip install rich
python3 interface_console.py
```

Dos jugadores se turnan en la misma máquina. En cada turno se pueden usar ítems
y luego elegir a quién disparar.

## Cómo regenerar la captura de la demo

```bash
python3 demo_consola.py
```

Genera `evidencia_tdd/06_captura_consola.svg` con una partida de ejemplo.

## Metodología TDD aplicada

Cada funcionalidad siguió el ciclo **Red → Green → Refactor**:

1. **Red:** se escriben primero las pruebas; al ejecutarlas fallan porque la
   funcionalidad aún no existe (ver `01_red.txt` y `03_red_semana2.txt`).
2. **Green:** se implementa el código mínimo hasta que todas pasan (ver
   `02_green.txt` y `04_green_semana2.txt`).
3. **Refactor:** se limpia el código (docstrings, constantes de clase, método
   interno `_cambiar_turno`, excepción `JugadaInvalida`) sin romper las pruebas.

Las pruebas son deterministas: el azar (`random.shuffle`, `random.choice`,
`random.randint`) se controla con `unittest.mock.patch`.

## Clases y conceptos principales

- `TipoBala` — cartuchos `REAL` / `FOGUEO`.
- `TipoItem` — `LUPA`, `CERVEZA`, `PASTILLA`, `BOTIQUIN`.
- `EstadoJuego` — `EN_CURSO` / `TERMINADO`.
- `JugadaInvalida` — excepción para el control de errores.
- `Jugador` — HP e inventario de ítems.
- `Escopeta` — carga, dispara, espía.
- `Juego` — turnos, ítems, **puntaje**, **estados** y **finalización** (partida
  al mejor de N asaltos).

## Mejoras planeadas (Semana 3)

- Ítems avanzados: Inversor y Esposas.
- Interfaz gráfica con `tkinter` ambientada.
