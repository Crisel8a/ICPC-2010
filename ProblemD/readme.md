<h1 align="center">
  <a href="#">
    Problem B
  </a>
</h1>

<p align="center">
  <strong>Conquista de castillos</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>

## Contexto

Durante la Edad Media, conquistar una región implicaba capturar sus castillos y dejar suficientes soldados para defenderlos. El tamaño inicial del ejército era importante porque, después de cada ataque, algunos soldados morían y otros debían permanecer en el castillo conquistado.

En este problema existe una región con varios castillos conectados mediante rutas bidireccionales. Debemos determinar el tamaño mínimo de un ejército capaz de capturar y mantener todos los castillos.

---

## Estructura de la región

Hay `n` castillos numerados desde `1` hasta `n`.

Entre cualquier par de castillos existe exactamente una ruta posible. Esto significa que el grafo de castillos es un **árbol**:

- Es conexo.
- Tiene `n` nodos.
- Tiene `n - 1` rutas.
- No contiene ciclos.

Cada ruta puede recorrerse como máximo dos veces:

- Una vez en una dirección.
- Una vez en la dirección contraria.

El ejército puede comenzar atacando cualquier castillo, sin importar cómo llegó inicialmente hasta allí.

---

## Información de cada castillo

Cada castillo `i` tiene tres valores:

```text
aᵢ, mᵢ, gᵢ
```

Donde:

- `aᵢ`: soldados mínimos necesarios para iniciar y ganar el ataque.
- `mᵢ`: soldados que morirán durante el ataque.
- `gᵢ`: soldados que deberán quedarse para defender el castillo.

Después de capturarlo, el ejército móvil pierde:

```text
mᵢ + gᵢ
```

soldados. Los muertos se pierden permanentemente y los guardias ya no continúan con el ejército.

Antes de atacar también deben existir suficientes soldados para cubrir ambas pérdidas. Por eso, para conquistar solamente el castillo `i`, el ejército necesita al menos:

```text
max(aᵢ, mᵢ + gᵢ)
```

---

## Reglas de movimiento y conquista

1. El primer castillo puede ser cualquiera.
2. Para atacar un castillo todavía no capturado, el ejército debe llegar hasta él mediante una ruta desde su posición actual.
3. Se puede pasar sin peligro por castillos que ya fueron capturados.
4. Una ruta no puede utilizarse más de una vez en cada dirección.
5. Después de cada ataque, el ejército móvil disminuye en `mᵢ + gᵢ` soldados.
6. Deben capturarse y mantenerse todos los castillos.

---

## Objetivo

Encontrar la cantidad mínima de soldados con la que debe comenzar el ejército para que exista:

- Un castillo inicial.
- Un orden de conquista.
- Un recorrido válido por las rutas.

que permita conquistar todos los castillos.

Solo se pide el tamaño mínimo del ejército, no el recorrido ni el orden utilizado.

---

## Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con:

```text
n
```

Donde:

```text
1 ≤ n ≤ 100
```

A continuación aparecen `n` líneas, una por castillo, con:

```text
a m g
```

Restricciones:

```text
1 ≤ a ≤ 1000
0 ≤ m ≤ a
1 ≤ g ≤ 1000
```

Los castillos se describen en orden, desde el castillo `1` hasta el castillo `n`.

Después aparecen `n - 1` líneas. Cada una contiene:

```text
u v
```

Esto indica que existe una ruta directa y bidireccional entre los castillos `u` y `v`.

La entrada termina con:

```text
0
```

---

## Formato de salida

Para cada caso se imprime:

```text
Case k: respuesta
```

Donde:

- `k` es el número del caso, comenzando en `1`.
- `respuesta` es el tamaño mínimo del ejército inicial.

---

## Ejemplo

### Entrada

```text
3
5 5 5
10 5 5
5 1 1
1 3
2 3
5
10 5 10
20 10 5
10 10 5
5 5 5
20 0 10
1 2
1 3
1 4
3 5
0
```

### Salida

```text
Case 1: 22
Case 2: 65
```

---

## Observaciones importantes

### El ejército siempre disminuye

Capturar un castillo nunca aumenta el ejército móvil. Cada conquista consume:

```text
pérdidaᵢ = mᵢ + gᵢ
```

Por eso el orden importa. Un castillo con un requisito alto puede necesitar ser conquistado antes de que el ejército pierda demasiados soldados.

### Elegir el castillo inicial equivale a enraizar el árbol

Si elegimos un castillo como inicio, podemos verlo como la raíz del árbol.

Para llegar por primera vez a un castillo descendiente, antes debemos haber capturado su padre. Además, debido al límite de dos recorridos por ruta, cada subárbol debe conquistarse como un bloque:

1. Entramos al subárbol.
2. Capturamos todos sus castillos.
3. Regresamos por la misma ruta, salvo que sea el último subárbol visitado.

De esta forma, el recorrido se comporta como una búsqueda en profundidad con un orden elegible para los hijos de cada nodo.

---

## Decisión de la solución

La solución utiliza **programación dinámica sobre árboles**.

Cada subárbol se resume mediante dos números:

```text
need: soldados mínimos necesarios para conquistar el subárbol
loss: soldados que se pierden después de conquistarlo completo
```

Este resumen permite tratar todo un subárbol como una sola tarea.

---

## 1. Resumen de un castillo individual

Para un castillo con valores `(a, m, g)`:

```text
loss = m + g
need = max(a, loss)
```

Se usa el máximo porque:

- Debemos cumplir el requisito `a` para atacar.
- También deben existir suficientes soldados para cubrir las muertes y los guardias.

---

## 2. Combinar dos tareas

Supongamos que una tarea `A` tiene:

```text
(needA, lossA)
```

y después realizamos una tarea `B`:

```text
(needB, lossB)
```

Para ejecutar `A` necesitamos `needA` soldados. Después de `A` habremos perdido `lossA`, así que para poder comenzar `B` necesitamos haber iniciado con:

```text
lossA + needB
```

El resumen de ejecutar `A` y después `B` es:

```text
need = max(needA, lossA + needB)
loss = lossA + lossB
```

Esta fórmula permite combinar secuencias completas de conquistas.

---

## 3. Orden óptimo de los subárboles

Los subárboles hijos pueden conquistarse en diferentes órdenes. Necesitamos encontrar el orden que minimiza `need`.

Para una tarea definimos su margen o prioridad como:

```text
priority = need - loss
```

Los subárboles deben procesarse en orden descendente de:

```text
need - loss
```

Es decir, primero se realizan las tareas que necesitan conservar más soldados por encima de lo que consumirán.

### Justificación mediante intercambio

Sean dos tareas `A` y `B` y supongamos que:

```text
needA - lossA ≥ needB - lossB
```

Si hacemos `A` antes que `B`, el requisito es:

```text
max(needA, lossA + needB)
```

Con la desigualdad anterior puede demostrarse que este valor nunca es mayor que el requisito de realizar `B` antes que `A`.

Por tanto, si dos tareas aparecen en el orden contrario, intercambiarlas no empeora la solución. Aplicando intercambios sucesivos obtenemos el orden óptimo descendente por `need - loss`.

---

## 4. DP para una raíz fija

Elegimos temporalmente un castillo como raíz.

Una función DFS calcula el par `(need, loss)` de cada subárbol:

1. Inicializa el resumen con el castillo actual.
2. Calcula recursivamente el resumen de cada hijo.
3. Ordena los hijos por `need - loss` descendente.
4. Combina los hijos, uno por uno, usando la fórmula anterior.
5. Devuelve el resumen completo del subárbol.

El valor `need` obtenido para la raíz es el tamaño mínimo del ejército si comenzamos en ese castillo.

---

## 5. Probar todos los castillos iniciales

El problema permite comenzar en cualquier castillo y `n ≤ 100`.

La alternativa más sencilla y segura es:

```text
para cada castillo root:
    calcular la DP usando root como raíz

respuesta = mínimo need encontrado
```

No es necesario implementar una técnica más compleja de rerooting porque cien ejecuciones de DFS son suficientemente pequeñas.

---

## Pseudocódigo

```text
función dfs(node, parent):
    loss = muertos[node] + guardias[node]
    need = máximo(ataque[node], loss)

    children = lista vacía

    para cada vecino de node:
        si vecino != parent:
            child_need, child_loss = dfs(vecino, node)
            agregar (child_need, child_loss) a children

    ordenar children por (child_need - child_loss) descendente

    para cada child en children:
        need = máximo(need, loss + child_need)
        loss = loss + child_loss

    devolver need, loss


respuesta = infinito

para root desde 1 hasta n:
    root_need, root_loss = dfs(root, sin_padre)
    respuesta = mínimo(respuesta, root_need)
```

---

## Ejemplo del primer caso

El árbol es:

```text
1 — 3 — 2
```

Las pérdidas individuales son:

```text
Castillo 1: 5 + 5 = 10
Castillo 2: 5 + 5 = 10
Castillo 3: 1 + 1 = 2
```

Si comenzamos en el castillo `3`:

```text
need inicial del castillo 3 = max(5, 2) = 5
```

Después podemos conquistar los subárboles de los castillos `1` y `2`. Al combinar sus requisitos y pérdidas, el mínimo necesario es:

```text
22 soldados
```

Esto coincide con:

```text
Case 1: 22
```

---

## Estructuras de datos elegidas

### Lista de adyacencia

El árbol se almacena como una lista de vecinos:

```text
graph[u] = castillos conectados directamente con u
```

Es la representación adecuada porque el grafo solo tiene `n - 1` rutas.

Ventajas:

- Memoria `O(n)`.
- Recorrido DFS directo.
- Acceso sencillo a los hijos de cada nodo.

### Tuplas `(need, loss)`

Cada subárbol se resume con una tupla de dos enteros. No es necesario guardar el orden completo de conquista ni copiar listas de castillos.

### Recursión

La profundidad máxima del árbol es `100`, muy inferior al límite normal de recursión de Python. Una DFS recursiva mantiene el código claro y seguro.

---

## ¿Por qué Python?

Python es una buena elección porque:

1. `n ≤ 100`, por lo que probar las cien raíces es económico.
2. Las listas de adyacencia son sencillas de construir.
3. Las tuplas permiten resumir cada subárbol claramente.
4. `sort` implementa un ordenamiento eficiente.
5. La recursión máxima es pequeña.
6. Los enteros de Python no sufren desbordamiento.

El objetivo principal aquí es modelar correctamente el orden de las conquistas; no se necesitan estructuras de bajo nivel ni optimizaciones complicadas.

---

## Complejidad

### Para una raíz

La DFS visita los `n` castillos y las `n - 1` rutas.

Ordenar las listas de hijos cuesta, en conjunto:

```text
O(n log n)
```

en el peor caso, por ejemplo cuando un castillo está conectado con casi todos los demás.

### Para todas las raíces

Ejecutamos la DFS `n` veces:

```text
O(n² log n)
```

Con `n ≤ 100`, este costo es muy pequeño.

### Memoria

- Lista de adyacencia: `O(n)`.
- Pila recursiva: `O(n)`.
- Resúmenes y listas temporales: `O(n)`.

Memoria total:

```text
O(n)
```

---

## Argumento de corrección

### Lema 1: el par `(need, loss)` resume completamente un subárbol

El efecto de conquistar un subárbol sobre lo que venga después solo depende de:

- Cuántos soldados se necesitan al comenzar.
- Cuántos soldados se habrán perdido al terminar.

Por eso no se necesita recordar su recorrido interno una vez calculado el par.

### Lema 2: ordenar por `need - loss` descendente es óptimo

El argumento de intercambio muestra que, para dos tareas consecutivas, colocar primero la de mayor `need - loss` nunca requiere más soldados. Repitiendo este intercambio se obtiene un orden óptimo para todos los hijos.

### Lema 3: la DFS calcula el mínimo para una raíz fija

Por inducción sobre el tamaño del subárbol:

- Una hoja se calcula correctamente con `max(a, m + g)`.
- Suponiendo correctos los resúmenes de los hijos, ordenarlos óptimamente y combinarlos con el castillo actual produce el mínimo posible para todo el subárbol.

### Teorema

Todo recorrido válido tiene algún castillo inicial. La DP obtiene el mínimo para cada posible inicio y el algoritmo escoge el menor de todos. Por tanto, el resultado es el tamaño mínimo global del ejército.

---

## Casos especiales

La solución contempla:

- Un solo castillo.
- Un árbol en forma de camino.
- Un árbol en forma de estrella.
- Castillos con `m = 0`.
- Castillos cuyo requisito de ataque es menor que `m + g`.
- Diferentes raíces que producen el mismo resultado.
- Subárboles con igual valor `need - loss`; pueden aparecer en cualquier orden entre sí.

---

## Resumen

La clave consiste en ver cada subárbol como una tarea con:

```text
(soldados necesarios, soldados perdidos)
```

Para una raíz fija, los hijos se ordenan por `need - loss` descendente y se combinan mediante programación dinámica. Como cualquier castillo puede ser el primero y `n` es pequeño, se prueban todas las raíces.

La solución resultante es clara, correcta y suficientemente rápida en Python, con complejidad `O(n² log n)` y memoria `O(n)`.
