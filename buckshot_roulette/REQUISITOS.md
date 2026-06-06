# Requerimientos funcionales — Buckshot Roulette

Estado actualizado al cierre de la **Semana 2**.

## Semana 1 — Lógica base

| ID    | Requerimiento                                                | Estado     | Prueba                                       |
| ----- | ------------------------------------------------------------ | ---------- | -------------------------------------------- |
| RF-01 | Crear jugadores con HP máximo configurable.                  | Completado | `test_jugador_inicia_con_hp_maximo`          |
| RF-02 | Un jugador puede recibir daño y reducir su HP.               | Completado | `test_recibir_dano_reduce_hp`                |
| RF-03 | El HP nunca es menor que 0.                                  | Completado | `test_jugador_muere_con_hp_cero`             |
| RF-04 | El HP nunca supera su máximo al curarse.                     | Completado | `test_hp_no_supera_maximo_al_curar`          |
| RF-05 | La escopeta se carga con balas reales y de fogueo mezcladas. | Completado | `test_escopeta_carga_balas_correctas`        |
| RF-06 | Detectar cuándo la recámara está vacía.                      | Completado | `test_recamara_vacia_detectada`              |
| RF-07 | Disparar con la recámara vacía produce un error controlado.  | Completado | `test_disparar_escopeta_vacia_lanza_error`   |
| RF-08 | Una bala real resta 1 HP al blanco.                          | Completado | `test_disparo_bala_real_reduce_hp`           |
| RF-09 | Una bala de fogueo no resta HP.                              | Completado | `test_disparo_fogueo_no_reduce_hp`           |
| RF-10 | El turno pasa al oponente al disparar al oponente.           | Completado | `test_turno_alterna_al_disparar_al_oponente` |
| RF-11 | Dispararse con fogueo conserva el turno.                     | Completado | `test_fogueo_a_si_mismo_mantiene_turno`      |
| RF-12 | Rechazar objetivos de disparo inválidos.                     | Completado | `test_objetivo_invalido_lanza_error`         |
| RF-13 | Declarar un ganador cuando un jugador llega a 0 HP.          | Completado | `test_hay_ganador_cuando_oponente_muere`     |
| RF-14 | Revelar la próxima bala sin consumirla (base de la Lupa).    | Completado | `test_espiar_no_consume_bala`                |

## Semana 2 — Lógica principal e ítems

| ID    | Requerimiento                                                             | Estado     | Prueba                                                                                   |
| ----- | ------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------- |
| RF-15 | Repartir ítems por ronda con progresión 0/2/3/4 (reinicia por asalto).    | Completado | `TestProgresionItems`                                                                    |
| RF-16 | Implementar ítems: Lupa, Cerveza, Pastilla, Segueta (sin Botiquín).       | Completado | `TestEfectoItems`, `TestSegueta`                                                         |
| RF-17 | Inventario máximo de 4 ítems; los sobrantes se descartan.                 | Completado | `test_inventario_maximo_4_items`, `test_reparto_descarta_sobrantes_por_tope`             |
| RF-18 | Interfaz jugable por consola utilizando `rich`.                           | Completado | `interface_console.py`, `demo_consola.py`                                                |
| RF-21 | Cargar entre 2 y 8 cartuchos al azar por ronda.                           | Completado | `test_total_de_cartuchos_entre_2_y_8`                                                    |
| RF-22 | Cantidad de balas reales y de fogueo aleatoria (mínimo una de cada tipo). | Completado | `test_siempre_al_menos_una_real_y_una_fogueo`                                            |
| RF-23 | La Segueta aplica doble daño en el siguiente disparo y se consume.        | Completado | `test_segueta_dobla_dano_en_disparo_real`, `test_segueta_se_consume_aunque_salga_fogueo` |
| RF-24 | Al morir un jugador, se reinicia el asalto y se asigna un punto.          | Completado | `test_progresion_se_reinicia_tras_asalto`, `test_hp_se_reinicia_entre_asaltos`           |

### Actividades de la Semana 2 (PDF) cubiertas

| Actividad                 | Implementación / Prueba                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| Turnos                    | `Juego.jugador_actual`, `_cambiar_turno`; pruebas de alternancia            |
| Validación de jugadas     | `Juego.usar_item`, `disparar`; `TestValidacionYErrores`, `TestSegueta`      |
| Puntaje                   | `Juego.puntaje`, `finalizar_asalto`; `test_puntaje_aumenta_al_ganar_asalto` |
| Estados del juego         | `EstadoJuego`, `esta_terminado`; `TestEstadosYPuntaje`                      |
| Control de errores        | Excepción `JugadaInvalida`; `TestValidacionYErrores`                        |
| Condición de finalización | `Juego.ganador_partida`, `asaltos_para_ganar`; `test_partida_termina_*`     |

## Semana 3 (planificado)

| ID    | Requerimiento                                    | Estado    | Semana |
| ----- | ------------------------------------------------ | --------- | ------ |
| RF-19 | Implementar ítems avanzados (Esposas, Inversor). | Pendiente | S3     |
| RF-20 | Desarrollar interfaz gráfica con `tkinter`.      | Pendiente | S3     |

## Requerimientos no funcionales

* **RNF-01:** La lógica del juego está desacoplada de la interfaz (`game_logic.py` no depende de `rich` ni de `tkinter`).
* **RNF-02:** El código está estructurado mediante clases y enumeraciones para mejorar mantenibilidad.
* **RNF-03:** Se supera el mínimo requerido de pruebas unitarias. Actualmente se cuenta con **47 pruebas** (14 de Semana 1 y 33 de Semana 2).
* **RNF-04:** La lógica y las pruebas se ejecutan en Python 3.x estándar sin dependencias externas. Solo la interfaz de consola utiliza `rich`.
