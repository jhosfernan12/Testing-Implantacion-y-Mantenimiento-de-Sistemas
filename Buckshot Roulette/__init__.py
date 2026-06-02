test_disparar_escopeta_vacia_lanza_error (tests.test_game_logic.TestEscopeta.test_disparar_escopeta_vacia_lanza_error)
Disparar sin balas debe lanzar un error controlado. ... ok
test_escopeta_carga_balas_correctas (tests.test_game_logic.TestEscopeta.test_escopeta_carga_balas_correctas)
La recamara debe contener exactamente las balas que se cargaron. ... ok
test_espiar_no_consume_bala (tests.test_game_logic.TestEscopeta.test_espiar_no_consume_bala)
Espiar (lupa) revela la proxima bala SIN sacarla de la recamara. ... ok
test_recamara_vacia_detectada (tests.test_game_logic.TestEscopeta.test_recamara_vacia_detectada)
Una escopeta sin cargar debe reportarse como vacia. ... ok
test_disparo_bala_real_reduce_hp (tests.test_game_logic.TestJuego.test_disparo_bala_real_reduce_hp)
Disparar una bala REAL al oponente le quita 1 de HP. ... ok
test_disparo_fogueo_no_reduce_hp (tests.test_game_logic.TestJuego.test_disparo_fogueo_no_reduce_hp)
Disparar una bala de FOGUEO no quita HP a nadie. ... ok
test_fogueo_a_si_mismo_mantiene_turno (tests.test_game_logic.TestJuego.test_fogueo_a_si_mismo_mantiene_turno)
Dispararse a si mismo con FOGUEO conserva el turno (regla clasica). ... ok
test_hay_ganador_cuando_oponente_muere (tests.test_game_logic.TestJuego.test_hay_ganador_cuando_oponente_muere)
Cuando un jugador queda sin HP, el otro es declarado ganador. ... ok
test_objetivo_invalido_lanza_error (tests.test_game_logic.TestJuego.test_objetivo_invalido_lanza_error)
Un objetivo distinto de 'yo' u 'oponente' debe ser rechazado. ... ok
test_turno_alterna_al_disparar_al_oponente (tests.test_game_logic.TestJuego.test_turno_alterna_al_disparar_al_oponente)
Tras disparar al oponente el turno pasa al otro jugador. ... ok
test_hp_no_supera_maximo_al_curar (tests.test_game_logic.TestJugador.test_hp_no_supera_maximo_al_curar)
Curar nunca debe dejar al jugador por encima de su HP maximo. ... ok
test_jugador_inicia_con_hp_maximo (tests.test_game_logic.TestJugador.test_jugador_inicia_con_hp_maximo)
Un jugador nuevo debe iniciar con su HP al maximo. ... ok
test_jugador_muere_con_hp_cero (tests.test_game_logic.TestJugador.test_jugador_muere_con_hp_cero)
Cuando el HP llega a 0 el jugador deja de estar vivo. ... ok
test_recibir_dano_reduce_hp (tests.test_game_logic.TestJugador.test_recibir_dano_reduce_hp)
Recibir dano debe restar HP al jugador. ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.003s

OK
