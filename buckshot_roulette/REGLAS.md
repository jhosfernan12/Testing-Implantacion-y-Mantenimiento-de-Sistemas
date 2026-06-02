# Buckshot Roulette — Documento de reglas

## 1. Nombre del juego

**Buckshot Roulette** (edición de 2 jugadores).

## 2. Objetivo del juego

Dos jugadores se enfrentan en una ruleta rusa con una escopeta. La escopeta se
carga con una mezcla de cartuchos **reales** (hacen daño) y de **fogueo** (no
hacen daño). En su turno, cada jugador decide a quién dispara. Gana el último
jugador que quede con vida.

## 3. Roles del jugador

Ambos jugadores tienen el mismo rol: son tiradores. No hay computadora ni IA —
son **dos personas reales** jugando por turnos en la misma máquina.

Cada jugador tiene:

- Un **nombre**.
- Una cantidad de **puntos de vida (HP)**, por defecto 3.

## 4. Reglas principales

1. Al inicio de cada ronda, la escopeta se carga con una mezcla aleatoria de
   balas reales y de fogueo. Ningún jugador sabe el orden.
2. Los jugadores se turnan. En su turno, el jugador elige una de dos acciones:
   - **Disparar al oponente.**
   - **Dispararse a sí mismo.**
3. Al disparar sale la bala que está al frente de la recámara:
   - Si es **real**, el blanco pierde 1 de HP.
   - Si es **fogueo**, no pasa nada.
4. **Regla clave:** si un jugador se dispara a sí mismo y sale **fogueo**,
   **conserva su turno** y vuelve a jugar. En cualquier otro caso, el turno
   pasa al oponente.
5. Cuando la recámara se vacía, comienza una nueva ronda y la escopeta se
   recarga.
6. Los **ítems** (Lupa, Cerveza, Pastilla, etc.) se reparten al inicio de cada
   ronda y modifican la partida. *Se implementan a partir de la Semana 2.*

## 5. Condiciones de victoria, derrota y empate

- **Victoria:** un jugador gana cuando el oponente llega a **0 HP**.
- **Derrota:** un jugador pierde cuando su HP llega a 0.
- **Empate:** no existe empate. La partida siempre termina con un ganador, ya
  que solo un jugador puede quedarse sin vida a la vez.

## 6. Funcionalidades mínimas (Semana 1)

- Crear dos jugadores con HP.
- Cargar la escopeta con balas reales y de fogueo mezcladas.
- Disparar (a uno mismo o al oponente) y aplicar el daño correcto.
- Alternar turnos según la regla del fogueo.
- Detectar cuándo hay un ganador.
- Detectar cuándo la recámara está vacía.

## 7. Tipos de cartucho

| Tipo    | Efecto                         |
|---------|--------------------------------|
| Real    | Quita 1 de HP al blanco        |
| Fogueo  | No hace daño                   |
