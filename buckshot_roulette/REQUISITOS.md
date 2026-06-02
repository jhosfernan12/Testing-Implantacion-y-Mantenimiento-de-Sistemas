# Requerimientos funcionales — Buckshot Roulette

Lista de requerimientos funcionales del juego. Los marcados con ✅ ya están
implementados y probados en la Semana 1. Los marcados con 🔜 corresponden a
semanas posteriores.

## Semana 1 — Lógica base

| ID    | Requerimiento                                                                 | Estado | Prueba que lo cubre                          |
|-------|-------------------------------------------------------------------------------|--------|----------------------------------------------|
| RF-01 | El sistema debe crear jugadores con un HP máximo configurable.                | ✅     | `test_jugador_inicia_con_hp_maximo`          |
| RF-02 | Un jugador debe poder recibir daño y reducir su HP.                            | ✅     | `test_recibir_dano_reduce_hp`                |
| RF-03 | El HP de un jugador nunca debe ser menor que 0.                               | ✅     | `test_jugador_muere_con_hp_cero`             |
| RF-04 | El HP de un jugador nunca debe superar su máximo al curarse.                  | ✅     | `test_hp_no_supera_maximo_al_curar`          |
| RF-05 | La escopeta debe cargarse con balas reales y de fogueo mezcladas.             | ✅     | `test_escopeta_carga_balas_correctas`        |
| RF-06 | El sistema debe detectar cuándo la recámara está vacía.                       | ✅     | `test_recamara_vacia_detectada`              |
| RF-07 | Disparar con la recámara vacía debe producir un error controlado.             | ✅     | `test_disparar_escopeta_vacia_lanza_error`   |
| RF-08 | Una bala real debe restar 1 de HP al blanco.                                  | ✅     | `test_disparo_bala_real_reduce_hp`           |
| RF-09 | Una bala de fogueo no debe restar HP.                                         | ✅     | `test_disparo_fogueo_no_reduce_hp`           |
| RF-10 | El turno debe pasar al oponente al disparar al oponente.                       | ✅     | `test_turno_alterna_al_disparar_al_oponente` |
| RF-11 | Dispararse a sí mismo con fogueo debe conservar el turno.                      | ✅     | `test_fogueo_a_si_mismo_mantiene_turno`      |
| RF-12 | El sistema debe rechazar objetivos de disparo inválidos.                      | ✅     | `test_objetivo_invalido_lanza_error`         |
| RF-13 | El sistema debe declarar un ganador cuando un jugador llega a 0 HP.           | ✅     | `test_hay_ganador_cuando_oponente_muere`     |
| RF-14 | Revelar (espiar) la próxima bala no debe consumirla — base de la Lupa.        | ✅     | `test_espiar_no_consume_bala`                |

## Semanas posteriores (planeado)

| ID    | Requerimiento                                                                 | Estado | Semana |
|-------|-------------------------------------------------------------------------------|--------|--------|
| RF-15 | Repartir 1–2 ítems aleatorios a cada jugador al inicio de cada ronda.         | 🔜     | S2     |
| RF-16 | Implementar ítems: Lupa, Cerveza, Pastilla, Botiquín.                         | 🔜     | S2     |
| RF-17 | Inventario máximo de 4 ítems por jugador.                                     | 🔜     | S2     |
| RF-18 | Interfaz por consola con la librería `rich`.                                  | 🔜     | S2     |
| RF-19 | Ítems avanzados: Segueta y Esposas.                                           | 🔜     | S3     |
| RF-20 | Interfaz gráfica con `tkinter` ambientada.                                    | 🔜     | S3     |

## Requerimientos no funcionales

- **RNF-01:** La lógica del juego debe estar completamente separada de la
  interfaz (la lógica no importa `rich` ni `tkinter`).
- **RNF-02:** El código debe estar organizado en clases (`Jugador`, `Escopeta`,
  `Juego`).
- **RNF-03:** Debe haber un mínimo de 8 pruebas unitarias (actualmente hay 14).
- **RNF-04:** El proyecto debe ejecutarse sin errores con Python 3.x estándar,
  sin dependencias externas para la lógica ni las pruebas.
