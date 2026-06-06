# Buckshot Roulette — Documento de reglas

## 1. Nombre del juego
**Buckshot Roulette** (edición de 2 jugadores reales).

## 2. Objetivo
Dos jugadores se enfrentan en una ruleta rusa con una escopeta cargada con
cartuchos reales (hacen daño) y de fogueo (no hacen daño). Gana el último
jugador con vida. Cada jugador empieza con 3 HP. No hay empate.

## 3. Roles
Ambos son tiradores, en igualdad de condiciones, turnándose en la misma máquina.
No hay inteligencia artificial.

## 4. Reglas principales

1. **Carga de la escopeta:** al inicio de cada ronda se cargan **entre 2 y 8
   cartuchos al azar**, con una cantidad **aleatoria** de reales y de fogueo
   (siempre al menos 1 de cada tipo). Al iniciar la ronda se anuncian los
   totales (por ejemplo "5 CARTUCHOS · 3 REALES · 2 FOGUEO"), pero **el orden
   permanece oculto**, como en el juego real.
2. **Turno y acción:** en su turno, el jugador elige disparar al oponente o
   dispararse a sí mismo.
3. **Efecto de los cartuchos:** una bala real quita 1 HP al blanco; una de
   fogueo no hace daño.
4. **Conservación del turno (regla clave):** dispararse a sí mismo con fogueo
   conserva el turno. En cualquier otro caso el turno pasa al oponente.
5. **Nueva ronda:** cuando la recámara se vacía, se recarga (nueva cantidad
   aleatoria) y se reparten ítems nuevos.
6. **Puntaje y partida:** la partida se juega al mejor de varios asaltos. Un
   asalto se gana cuando el oponente llega a 0 HP; quien gana el asalto suma un
   punto. La partida termina cuando alguien alcanza los asaltos necesarios.

## 5. Ítems (Semana 2)

**El Botiquín fue retirado de esta versión.** Los ítems se reparten al inicio de
cada ronda siguiendo una **progresión por asalto** (se reinicia cada vez que un
jugador muere):

| Ronda del asalto | Ítems repartidos a cada jugador |
|------------------|---------------------------------|
| Ronda 1          | 0 (sin ítems)                   |
| Ronda 2          | 2                               |
| Ronda 3          | 3                               |
| Ronda 4 en adelante | 4                            |

Los ítems se eligen al azar y pueden repetirse. El inventario tiene un tope de 4;
si se reparten más de los que caben, los sobrantes se descartan. Al inicio de la
ronda se informa qué ítem recibió cada jugador.

| Ítem     | Efecto                                                                          |
|----------|---------------------------------------------------------------------------------|
| Lupa     | Revela el tipo de la próxima bala sin consumirla.                               |
| Cerveza  | Expulsa (descarta) la bala del frente sin disparar a nadie.                     |
| Pastilla | Recupera 1 HP. Al usarla se vuelve a mostrar el tablero para ver la curación.   |
| Segueta  | El **próximo disparo hace doble daño** (2 HP). Se gasta al disparar aunque salga fogueo. |

## 6. Condiciones de victoria, derrota y empate

- **Victoria:** ganar la cantidad de asaltos requerida.
- **Derrota:** que el oponente alcance esos asaltos primero.
- **Empate:** no existe.

## 7. Tipos de cartucho

| Tipo    | Efecto                                                                    |
|---------|---------------------------------------------------------------------------|
| Real    | Quita 1 HP al blanco (2 HP si la Segueta está activa).                     |
| Fogueo  | No hace daño. Si el tirador se disparó a sí mismo, además conserva el turno. |
