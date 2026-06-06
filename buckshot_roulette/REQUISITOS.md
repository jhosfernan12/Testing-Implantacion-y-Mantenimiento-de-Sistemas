# Requerimientos funcionales — Buckshot Roulette

Estado actualizado al cierre de la **Semana 2**.

## Semana 1 — Lógica base

| ID    | Requerimiento                                                       | Estado | Prueba                                       |
|-------|---------------------------------------------------------------------|--------|----------------------------------------------|
| RF-01 | Crear jugadores con HP máximo configurable.                         | ✅     | `test_jugador_inicia_con_hp_maximo`          |
| RF-02 | Un jugador puede recibir daño y reducir su HP.                      | ✅     | `test_recibir_dano_reduce_hp`                |
| RF-03 | El HP nunca es menor que 0.                                         | ✅     | `test_jugador_muere_con_hp_cero`             |
| RF-04 | El HP nunca supera su máximo al curarse.                            | ✅     | `test_hp_no_supera_maximo_al_curar`          |
| RF-05 | La escopeta se carga con balas reales y de fogueo mezcladas.        | ✅     | `test_escopeta_carga_balas_correctas`        |
| RF-06 | Detectar cuándo la recámara está vacía.                             | ✅     | `test_recamara_vacia_detectada`              |
| RF-07 | Disparar con la recámara vacía produce un error controlado.         | ✅     | `test_disparar_escopeta_vacia_lanza_error`   |
| RF-08 | Una bala real resta 1 HP al blanco.                                 | ✅     | `test_disparo_bala_real_reduce_hp`           |
| RF-09 | Una bala de fogueo no resta HP.                                     | ✅     | `test_disparo_fogueo_no_reduce_hp`           |
| RF-10 | El turno pasa al oponente al disparar al oponente.                  | ✅     | `test_turno_alterna_al_disparar_al_oponente` |
| RF-11 | Dispararse con fogueo conserva el turno.                            | ✅     | `test_fogueo_a_si_mismo_mantiene_turno`      |
| RF-12 | Rechazar objetivos de disparo inválidos.                           | ✅     | `test_objetivo_invalido_lanza_error`         |
| RF-13 | Declarar un ganador cuando un jugador llega a 0 HP.                 | ✅     | `test_hay_ganador_cuando_oponente_muere`     |
| RF-14 | Revelar la próxima bala sin consumirla (base de la Lupa).          | ✅     | `test_espiar_no_consume_bala`                |

## Semana 2 — Lógica principal e ítems

| ID    | Requerimiento                                                       | Estado | Prueba                                       |
|-------|---------------------------------------------------------------------|--------|----------------------------------------------|
| RF-15 | Repartir 1–2 ítems aleatorios a cada jugador por ronda.            | ✅     | `test_repartir_da_items_a_ambos_jugadores`   |
| RF-16 | Implementar ítems: Lupa, Cerveza, Pastilla, Segueta (sin Botiquín). | ✅     | `TestEfectoItems`, `TestSegueta`             |
| RF-17 | Inventario máximo de 4 ítems por jugador.                          | ✅     | `test_inventario_maximo_4_items`             |
| RF-18 | Interfaz jugable por consola usando `rich`.                        | ✅     | `interface_console.py` + `demo_consola.py`   |
| RF-21 | Cargar entre 2 y 8 cartuchos al azar por ronda.                    | ✅     | `test_total_de_cartuchos_entre_2_y_8`        |
| RF-22 | Cantidad de reales/fogueo aleatoria (mín. 1 de cada).              | ✅     | `test_siempre_al_menos_una_real_y_una_fogueo`|
| RF-23 | La Segueta hace doble daño en el próximo disparo y se consume.     | ✅     | `test_segueta_dobla_dano_en_disparo_real`, `test_segueta_se_consume_aunque_salga_fogueo` |

### Actividades de la Semana 2 (PDF) cubiertas

| Actividad                | Dónde se implementa / prueba                                              |
|--------------------------|---------------------------------------------------------------------------|
| Turnos                   | `Juego.jugador_actual`, `_cambiar_turno`; tests de alternancia            |
| Validación de jugadas    | `Juego.usar_item`, `disparar`; `TestValidacionYErrores`, `TestSegueta`    |
| Puntaje                  | `Juego.puntaje`, `finalizar_asalto`; `test_puntaje_aumenta_al_ganar_asalto`|
| Estados del juego        | `EstadoJuego`, `esta_terminado`; `TestEstadosYPuntaje`                     |
| Control de errores       | excepción `JugadaInvalida`; `TestValidacionYErrores`                       |
| Condición de finalización| `Juego.ganador_partida`, `asaltos_para_ganar`; `test_partida_termina_*`    |

## Semana 3 (planeado)

| ID    | Requerimiento                                  |      Estado        | Semana |
|-------|------------------------------------------------|--------------------|--------|
| RF-19 | Ítem avanzado adicional (Inversor y Esposas).  | (proximamente)     | S3     |
| RF-20 | Interfaz gráfica con `tkinter` ambientada.     | (proximamente)     | S3     |
| RF-21 | Sonidos para mayor inmersion                   | (proximamente)     | S3     |

## Requerimientos no funcionales

- **RNF-01:** La lógica está separada de la interfaz (`game_logic.py` no importa
  `rich` ni `tkinter`).
- **RNF-02:** Código organizado en clases y enums.
- **RNF-03:** Mínimo 8 pruebas unitarias. Actualmente hay **41** (14 de S1 + 27 de S2).
- **RNF-04:** La lógica y las pruebas corren con Python 3.x estándar sin
  dependencias externas. Solo la interfaz por consola usa `rich`.
