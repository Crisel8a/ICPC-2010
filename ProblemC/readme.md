<h1 align="center">
  <a href="#">
    Problem C
  </a>
</h1>

<p align="center">
  <strong>Stuck Squares — Bio-bots</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>

## Contexto

Los investigadores de **International Bio-bot Makers (IBM)** desarrollaron unos pequeños robots llamados **Bio-bots**. Sus motores y su capacidad de giro son limitados, por lo que dentro de una habitación solo pueden desplazarse:

- Hacia el **norte**.
- Hacia el **este**.

La habitación es una cuadrícula de `m × n` cuadrados. Un robot ocupa un cuadrado completo y debe alcanzar la salida situada en la esquina noreste. Algunos cuadrados contienen paredes y no pueden ser ocupados ni atravesados.

## Coordenadas y movimientos

La esquina suroeste tiene coordenadas `(0, 0)` y la esquina noreste tiene coordenadas `(n - 1, m - 1)`.

Desde `(x, y)` solo se permiten:

```text
Norte: (x, y + 1)
Este:  (x + 1, y)
```

El robot nunca puede moverse hacia el sur ni hacia el oeste.

## Paredes

Cada pared es un segmento horizontal descrito por:

```text
x1 y1 x2 y2
```

con:

```text
0 ≤ x1 ≤ x2 < n
0 ≤ y1 = y2 < m
```

La pared ocupa todos los cuadrados desde `(x1, y1)` hasta `(x2, y1)`, incluidos sus extremos. Puede ocupar un solo cuadrado si `x1 = x2`. Las paredes no se superponen.

## ¿Qué es un stuck square?

Un cuadrado libre es un **stuck square** si un Bio-bot que comienza allí no puede llegar a la salida mediante ninguna secuencia de movimientos hacia el norte o el este.

Los cuadrados ocupados por paredes no se cuentan como stuck squares, porque un robot no puede comenzar en ellos.

## Objetivo

Para cada habitación, contar cuántos cuadrados libres no tienen ningún camino válido hasta la salida.

---

## Formato de entrada

La entrada contiene varios casos de prueba. Cada caso comienza con:

```text
m n w
```

Donde:

- `m`: número de filas.
- `n`: número de columnas.
- `w`: número de paredes horizontales.

Restricciones:

```text
0 ≤ m, n ≤ 10⁶
0 ≤ w ≤ 1000
```

A continuación aparecen `w` líneas con:

```text
x1 y1 x2 y2
```

La entrada termina con:

```text
0 0 0
```

Esta línea no pertenece a ningún caso.

## Formato de salida

Para cada caso se imprime:

```text
Case k: respuesta
```

`k` comienza en `1` y `respuesta` es el número de stuck squares.

## Ejemplo

### Entrada

```text
8 8 3
1 6 3 6
2 4 2 4
4 2 7 2
0 0 0
```

### Salida

```text
Case 1: 8
```

---

## Dificultad principal

Una programación dinámica sobre todos los cuadrados necesitaría procesar `m × n` posiciones. Esto es imposible porque:

```text
m × n ≤ 10¹²
```

Sin embargo, solo existen hasta `1000` paredes. La habitación es enorme, pero su estructura cambia en muy pocas coordenadas.

## Decisión de la solución

La solución propuesta combina:

1. **Compresión de coordenadas**.
2. **Programación dinámica** desde la salida.
3. **Conteo por áreas** de las regiones comprimidas.
4. `bytearray` para almacenar estados booleanos con poca memoria.

No se construirá la cuadrícula original.

---

## 1. Compresión de coordenadas

Solo necesitamos conservar las posiciones donde comienza o termina una pared.

Para el eje `x` guardamos:

```text
0
n
x1 de cada pared
x2 + 1 de cada pared
```

Para el eje `y` guardamos:

```text
0
m
y de cada pared
y + 1 de cada pared
```

Se utiliza `x2 + 1` porque el extremo `x2` está incluido en la pared. La coordenada adicional crea una frontera inmediatamente después del segmento. De forma similar, `y + 1` separa la fila de la pared de la región situada al norte.

Ordenamos las coordenadas y eliminamos duplicados. Cada par de coordenadas consecutivas delimita una región rectangular de la cuadrícula original.

Si:

```text
xs[i] = 10
xs[i + 1] = 25
```

la columna comprimida representa las columnas originales `10` hasta `24` y tiene anchura `15`.

### Tamaño comprimido

Cada pared añade como máximo dos fronteras por eje, así que:

```text
X ≤ 2w + 1
Y ≤ 2w + 1
```

Para `w = 1000`:

```text
X × Y ≤ 2001 × 2001 = 4 004 001
```

Esto reduce una cuadrícula potencial de un billón de cuadrados a unos cuatro millones de regiones.

---

## 2. Representación de las paredes

Cada pared se transforma en una o varias celdas consecutivas de la cuadrícula comprimida.

Se utilizará una matriz de `bytearray`:

```text
blocked[y][x] = 1  si la región contiene una pared
blocked[y][x] = 0  si la región está libre
```

`bytearray` utiliza aproximadamente un byte por posición. Una lista normal de valores booleanos de Python consumiría bastante más memoria debido a sus referencias internas.

---

## 3. Programación dinámica

Definimos una región como **alcanzable** si desde ella existe un camino hasta la salida.

Una región libre puede alcanzar la salida si:

1. Contiene la salida.
2. Su región vecina al norte puede alcanzarla.
3. Su región vecina al este puede alcanzarla.

La transición conceptual es:

```text
reachable[y][x] =
    no_bloqueada[y][x]
    y (
        contiene_la_salida
        o reachable[y + 1][x]
        o reachable[y][x + 1]
      )
```

Como un estado depende del norte y del este, procesamos desde la esquina noreste hacia la suroeste:

- Filas de norte a sur.
- Columnas de este a oeste.

## Optimización de memoria

Para calcular una fila solo necesitamos:

- La fila situada al norte.
- El estado situado al este dentro de la fila actual.

Por eso no guardamos toda la matriz `reachable`. Solo mantenemos:

```text
north_row
current_row
```

Ambas se almacenan como `bytearray`, reduciendo la memoria adicional de la DP a `O(X)`.

---

## 4. Conteo mediante áreas

Una celda comprimida puede representar muchos cuadrados originales.

Para la región `(x, y)`:

```text
ancho = xs[x + 1] - xs[x]
alto  = ys[y + 1] - ys[y]
área  = ancho × alto
```

Si la región no está bloqueada y no alcanza la salida, se suma su área completa a la respuesta. Las regiones ocupadas por paredes se ignoran.

---

## Pseudocódigo

```text
para cada caso:
    leer m, n, w
    leer las paredes

    xs = {0, n}
    ys = {0, m}

    para cada pared (x1, y, x2, y):
        agregar x1 y x2 + 1 a xs
        agregar y y y + 1 a ys

    ordenar xs y ys
    crear índices de coordenadas

    crear blocked como matriz de bytearray
    marcar las paredes comprimidas

    north_row = todo falso
    stuck = 0

    para y desde norte hasta sur:
        current_row = todo falso

        para x desde este hasta oeste:
            si está bloqueada:
                continuar

            reachable =
                contiene la salida
                o north_row[x]
                o current_row[x + 1]

            current_row[x] = reachable

            si no es reachable:
                stuck += ancho_real × alto_real

        north_row = current_row

    imprimir stuck
```

---

## Por qué la compresión es válida

Las coordenadas se dividen exactamente donde aparece o desaparece una pared. Dentro de un mismo rectángulo comprimido no cambia la distribución de obstáculos.

Todas sus celdas pueden desplazarse internamente hacia el norte o el este. Si existe una salida válida por alguno de esos límites, todas pueden alcanzarla; si ninguno de los límites conduce a la salida, ninguna puede escapar.

Por tanto, todas las celdas de una región comprimida comparten el mismo estado y pueden procesarse juntas.

## Argumento de corrección de la DP

Cuando procesamos una región, los estados de sus vecinos norte y este ya son conocidos.

- Si contiene una pared, no puede ser ocupada.
- Si es la salida, es alcanzable.
- Si el norte o el este son alcanzables, la región también lo es con un movimiento inicial hacia ese vecino.
- Si ninguno es alcanzable, no existe otro primer movimiento permitido y la región está atascada.

La transición considera exactamente todas las posibilidades de movimiento. Al sumar el área de cada región libre no alcanzable, contamos cada stuck square una única vez.

---

## Complejidad

Sean `X` y `Y` las cantidades de intervalos comprimidos. Ambas son `O(w)`.

### Tiempo

- Ordenar coordenadas: `O(w log w)`.
- Marcar paredes: `O(w²)` en el peor caso.
- Programación dinámica: `O(XY) = O(w²)`.

Complejidad total:

```text
O(w²)
```

### Memoria

- Regiones bloqueadas: `O(XY) = O(w²)` bytes con `bytearray`.
- Filas de la DP: `O(X) = O(w)`.
- Coordenadas y paredes: `O(w)`.

Complejidad total:

```text
O(w²)
```

---

## ¿Por qué Python?

Python es adecuado porque el algoritmo no procesa `m × n`, sino como máximo alrededor de cuatro millones de regiones comprimidas.

Además:

- `set` y `sorted` simplifican la compresión de coordenadas.
- Los diccionarios permiten traducir coordenadas a índices en `O(1)` promedio.
- `bytearray` almacena millones de estados de forma compacta.
- Los enteros de Python tienen precisión arbitraria y pueden contar áreas de hasta `10¹²` sin desbordamiento.

Para conservar el rendimiento, no se crean objetos o nodos por región. Se utilizan índices enteros, listas de coordenadas y arreglos compactos.

## Estructuras de datos elegidas

| Información | Estructura | Motivo |
|---|---|---|
| Coordenadas relevantes | `set` y lista ordenada | Eliminar duplicados y formar intervalos |
| Coordenada a índice | `dict` | Búsqueda promedio `O(1)` |
| Paredes originales | Lista de tuplas | Solo existen hasta 1000 |
| Regiones bloqueadas | Lista de `bytearray` | Aproximadamente un byte por región |
| Estado de alcanzabilidad | Dos `bytearray` | Solo se necesitan dos filas |
| Respuesta | Entero de Python | Evita desbordamiento con áreas grandes |

## Casos especiales

La solución debe contemplar:

- Habitación sin paredes: la respuesta es `0`.
- Pared de un solo cuadrado.
- Varias paredes en una misma fila.
- Paredes que tocan los bordes.
- Salida ocupada: todos los cuadrados libres quedan atascados.
- Regiones comprimidas que representan millones de cuadrados.
- Múltiples casos de prueba.

## Resumen

La cuadrícula original es demasiado grande para representarla. La clave es conservar únicamente las coordenadas donde cambian las paredes.

La compresión reduce el problema a `O(w²)` regiones. Una programación dinámica desde el noreste determina cuáles alcanzan la salida, y el área de las regiones restantes produce la cantidad exacta de stuck squares.

Esta estrategia es suficientemente eficiente y utiliza estructuras especialmente apropiadas para Python.
