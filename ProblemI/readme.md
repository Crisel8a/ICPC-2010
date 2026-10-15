# Ice Festival Tour

## 1. Contexto del problema

El equipo de programación de la Arctic University quiere organizar un festival de esculturas de hielo. Para obtener el hielo, planea cortar bloques de un lago congelado.

Antes de hacerlo, un robot ligero debe inspeccionar el grosor del hielo en una cuadrícula rectangular. El robot visita las casillas una por una y envía tres reportes de progreso cuando ha completado aproximadamente:

- un cuarto del recorrido;
- la mitad del recorrido;
- tres cuartos del recorrido.

Los lugares desde los que debe enviar esos reportes se proporcionan como tres **puntos de control** o *check-in points*.

## 2. ¿Qué recorrido debe hacer el robot?

El robot debe cumplir todas estas reglas:

1. Comenzar en la esquina inferior izquierda `(0, 0)`.
2. Terminar en la casilla `(0, 1)`.
3. Visitar **todas las casillas exactamente una vez**.
4. Moverse una casilla por turno.
5. Moverse únicamente en las cuatro direcciones cardinales:
   - norte;
   - sur;
   - este;
   - oeste.
6. Visitar cada punto de control en el momento exacto indicado.

Un camino que visita todos los vértices de un grafo exactamente una vez se llama **camino hamiltoniano**. Por tanto, el problema pide contar caminos hamiltonianos de la cuadrícula que, además, respeten posiciones obligatorias en tiempos determinados.

## 3. Sistema de coordenadas

Cada casilla se identifica mediante:

```text
(fila, columna)
```

- La fila `0` es la fila inferior.
- La columna `0` es la columna izquierda.
- El inicio siempre es `(0, 0)`.
- El final siempre es `(0, 1)`.

Para una cuadrícula de `m` filas y `n` columnas:

```text
0 <= fila < m
0 <= columna < n
```

## 4. Numeración de los pasos

La casilla inicial cuenta como la primera casilla visitada:

```text
paso 1 = (0, 0)
```

Si el tablero contiene:

```text
total = m * n
```

casillas, los tres puntos de control deben visitarse en los pasos:

```text
t1 = floor(1 * total / 4)
t2 = floor(2 * total / 4)
t3 = floor(3 * total / 4)
```

El robot debe llegar al destino `(0, 1)` en:

```text
t4 = total
```

La división es entera. En Python se expresa con `//`:

```python
t1 = total // 4
t2 = (2 * total) // 4
t3 = (3 * total) // 4
```

## 5. Objetivo

Para cada caso de prueba debemos calcular cuántos recorridos diferentes:

- comienzan en `(0, 0)`;
- terminan en `(0, 1)`;
- visitan cada casilla exactamente una vez;
- se mueven solo entre casillas vecinas;
- visitan los tres puntos de control en sus pasos exactos.

Puede haber:

- ningún recorrido válido;
- un único recorrido;
- varios recorridos diferentes.

## 6. Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con:

```text
m n
```

donde:

- `m` es la cantidad de filas;
- `n` es la cantidad de columnas;
- `2 <= m, n <= 8`.

La siguiente línea contiene seis enteros:

```text
r1 c1 r2 c2 r3 c3
```

Estos valores representan, en orden, los tres puntos de control:

```text
(r1, c1), (r2, c2), (r3, c3)
```

Cada coordenada cumple:

```text
0 <= ri < m
0 <= ci < n
```

La entrada termina con:

```text
0 0
```

Esta línea no representa un caso de prueba y no está seguida por puntos de control.

## 7. Formato de salida

Para cada caso se imprime:

```text
Case k: respuesta
```

donde:

- `k` comienza en `1`;
- `respuesta` es el número de recorridos válidos.

## 8. Ejemplo

### Entrada

```text
3 6
2 1 2 4 0 4
4 3
2 0 3 2 0 2
0 0
```

### Salida

```text
Case 1: 2
Case 2: 0
```

### Explicación del primer caso

La cuadrícula tiene:

```text
3 * 6 = 18 casillas
```

Los tiempos obligatorios son:

```text
t1 = floor(18 / 4)     = 4
t2 = floor(36 / 4)     = 9
t3 = floor(54 / 4)     = 13
t4 = 18
```

El robot debe:

- estar en `(2, 1)` en el paso `4`;
- estar en `(2, 4)` en el paso `9`;
- estar en `(0, 4)` en el paso `13`;
- terminar en `(0, 1)` en el paso `18`.

Existen exactamente dos recorridos que cumplen todo, por eso la respuesta es `2`.

En el segundo caso no existe ningún recorrido válido, por eso se imprime `0`.

## 9. ¿Por qué no se prueban todas las permutaciones?

Un tablero de `8 × 8` contiene `64` casillas. Probar todas las posibles ordenaciones requeriría considerar hasta `64!` secuencias, una cantidad imposible de manejar.

Además, no cualquier orden sirve: dos casillas consecutivas deben ser vecinas. Conviene construir el camino desde el inicio y probar solamente movimientos válidos.

La técnica apropiada es **DFS con backtracking**:

1. Marcamos la casilla actual como visitada.
2. Probamos cada vecino que todavía no fue visitado.
3. Continuamos recursivamente.
4. Al regresar, desmarcamos la casilla para probar otra opción.

Sin embargo, incluso esta búsqueda puede crecer demasiado. Por eso se agregan varias **podas** que detectan cuanto antes los caminos que ya no pueden completarse.

## 10. Estructuras de datos elegidas

### Matriz o lista de visitados

Se necesita saber en tiempo constante si una casilla ya fue utilizada:

```text
visitado[fila][columna]
```

Antes de entrar a una casilla se marca como visitada. Al retroceder en el backtracking se desmarca.

### Lista de vecinos

Para cada casilla podemos precalcular sus vecinos válidos. Cada casilla tiene como máximo cuatro:

```text
arriba, abajo, izquierda, derecha
```

Esto evita recalcular límites en cada llamada recursiva.

### Arreglo de posiciones obligatorias

Guardamos las cuatro metas temporales:

```text
(t1, punto_1)
(t2, punto_2)
(t3, punto_3)
(total, destino)
```

Así es fácil saber cuál es la siguiente posición que el robot debe alcanzar y cuánto tiempo le queda.

### Cola para comprobar conectividad

Una búsqueda BFS pequeña permite verificar que todas las casillas sin visitar continúan formando una sola región accesible.

Como hay como máximo `64` casillas, esta comprobación es económica y elimina muchas ramas imposibles.

## 11. Algoritmo paso a paso

### Paso 1: calcular los tiempos obligatorios

Para `total = m * n` calculamos:

```text
t1 = total // 4
t2 = (2 * total) // 4
t3 = (3 * total) // 4
t4 = total
```

Asociamos cada tiempo con su posición requerida.

### Paso 2: comenzar en `(0, 0)`

La búsqueda empieza con:

```text
posición = (0, 0)
paso = 1
```

La casilla inicial se marca como visitada.

### Paso 3: comprobar el tiempo actual

Si el paso actual tiene una posición obligatoria, el robot debe estar exactamente en ella.

Si está en otra casilla, la rama se descarta inmediatamente.

También evitamos entrar antes de tiempo a:

- un punto de control futuro;
- la casilla final `(0, 1)`.

Como cada casilla solo puede visitarse una vez, entrar antes impediría volver en el momento requerido.

### Paso 4: comprobar si la siguiente meta todavía es alcanzable

Sea `objetivo` la siguiente posición obligatoria y sea:

```text
movimientos_disponibles = tiempo_objetivo - paso_actual
```

Calculamos la distancia Manhattan:

```text
distancia = abs(fila - fila_objetivo)
          + abs(columna - columna_objetivo)
```

Si:

```text
distancia > movimientos_disponibles
```

ya no hay tiempo suficiente para llegar y se poda la rama.

### Paso 5: comprobar la paridad

La cuadrícula es un grafo bipartito: cada movimiento cambia el color de la casilla si imaginamos el tablero como un ajedrez.

Por ello, además de alcanzar la meta en distancia, debe cumplirse:

```text
(movimientos_disponibles - distancia) es par
```

Si la diferencia es impar, es imposible llegar a esa posición exactamente en el tiempo requerido.

### Paso 6: comprobar que el área restante sigue conectada

Las casillas sin visitar deben permanecer conectadas.

Si el camino ya construido divide las casillas restantes en dos regiones, el robot podría recorrer una de ellas, pero después no podría cruzar las casillas ya visitadas para llegar a la otra.

Una BFS sobre las casillas libres detecta este caso y permite abandonar la rama.

### Paso 7: detectar callejones sin salida

Una casilla libre que no sea el destino necesita formar parte del camino restante.

Si ya no tiene salidas disponibles, el recorrido es imposible. Si solo tiene una salida, puede convertirse en un movimiento forzado:

- debe visitarse inmediatamente desde la posición actual; o
- quedará aislada y nunca podrá incluirse en el recorrido.

Esta poda evita crear casillas encerradas que el robot tendría que visitar más tarde.

### Paso 8: probar los siguientes movimientos

Se recorren los vecinos no visitados de la posición actual.

Para cada candidato válido:

1. se marca como visitado;
2. se llama recursivamente con `paso + 1`;
3. se acumula la cantidad de recorridos encontrados;
4. se desmarca al regresar.

### Paso 9: reconocer una solución

Cuando `paso == total`, el camino solo es válido si la posición actual es `(0, 1)`.

Como nunca se permite repetir una casilla, haber llegado al paso `total` significa que todas las casillas fueron visitadas exactamente una vez.

## 12. Podas utilizadas

### Poda 1: tiempo y posición obligatoria

En un tiempo de control, cualquier posición diferente de la requerida es inválida.

### Poda 2: punto de control visitado antes de tiempo

Una posición obligatoria futura no puede utilizarse antes de su turno, porque no podría visitarse nuevamente.

### Poda 3: distancia insuficiente

Si la distancia Manhattan supera los movimientos disponibles, no es posible alcanzar la siguiente meta.

### Poda 4: paridad incompatible

Aunque haya pasos suficientes, la alternancia de colores puede impedir llegar exactamente en el paso necesario.

### Poda 5: destino prematuro

No se puede entrar en `(0, 1)` antes del último paso.

### Poda 6: región restante desconectada

Si las casillas libres quedan divididas, una parte será inaccesible después de recorrer la otra.

### Poda 7: casilla libre atrapada

Si una casilla que todavía debe visitarse queda sin conexiones útiles, el camino no podrá completarse.

### Poda 8: incompatibilidad global de colores

El inicio `(0, 0)` y el final `(0, 1)` tienen colores opuestos. Un camino entre colores opuestos utiliza una cantidad impar de movimientos.

Como el recorrido completo usa `m * n - 1` movimientos, si `m * n` es impar no puede existir ninguna solución.

## 13. ¿Por qué funciona?

### Invariante del backtracking

En cada llamada recursiva:

- el camino comienza en `(0, 0)`;
- todas sus casillas son diferentes;
- cada par de casillas consecutivas es adyacente;
- `paso` coincide con la cantidad de casillas visitadas.

El invariante se conserva porque únicamente avanzamos a vecinos no visitados.

### La búsqueda no omite recorridos válidos

Desde cada estado se prueban todos los vecinos no visitados que todavía pueden pertenecer a una solución. Por tanto, cualquier recorrido válido corresponde a una secuencia de decisiones explorada por el DFS.

Las podas solo eliminan estados matemáticamente imposibles:

- no pueden cumplir un tiempo obligatorio;
- no pueden alcanzar la siguiente meta;
- tienen paridad incorrecta;
- dejaron casillas desconectadas o atrapadas;
- llegaron demasiado pronto al destino.

Ninguna de estas situaciones puede formar parte de una solución válida.

### Cada recorrido se cuenta una sola vez

Cada recorrido completo corresponde a una secuencia única de movimientos desde `(0, 0)`. El DFS genera esa secuencia una sola vez, así que no hay duplicados.

### Conclusión

El algoritmo explora todos y solo los recorridos que pueden satisfacer las reglas, y suma uno exactamente cuando se visita toda la cuadrícula y se termina en `(0, 1)`. Por tanto, la respuesta calculada es correcta.

## 14. Complejidad

Sea:

```text
N = m * n
```

con `N <= 64`.

### Tiempo

Contar caminos hamiltonianos es un problema exponencial. En el peor caso, cada estado puede probar hasta cuatro movimientos:

```text
O(4^N)
```

Si se realiza una BFS de hasta `N` casillas en cada estado, una cota conservadora es:

```text
O(N * 4^N)
```

Esta cota teórica es muy grande, pero no representa el comportamiento práctico: los puntos de control y las podas eliminan la mayoría de las ramas mucho antes de alcanzar profundidad `N`.

No es correcto afirmar que la solución es polinómica; la eficiencia práctica proviene del backtracking fuertemente podado.

### Memoria

Se almacenan:

- la cuadrícula y sus vecinos: `O(N)`;
- las casillas visitadas: `O(N)`;
- la pila recursiva: como máximo `O(N)`;
- una cola temporal para BFS: `O(N)`.

Por tanto, la memoria total es:

```text
O(N)
```

## 15. ¿Por qué Python?

Python es adecuado para presentar esta solución porque permite implementar con claridad:

- DFS recursivo;
- backtracking mediante marcado y desmarcado;
- listas de vecinos;
- BFS con `deque`;
- enteros de tamaño arbitrario para contar recorridos.

La parte delicada no es una operación numérica pesada, sino reducir el árbol de búsqueda con buenas podas. Para tableros de hasta `8 × 8`, una implementación cuidadosa en Python puede ser apropiada.

Si posteriormente se necesita el máximo rendimiento posible, C++ sería una alternativa natural por su menor coste por llamada recursiva. Sin embargo, Python resulta más sencillo para aprender y explicar primero la lógica.

## 16. Casos especiales

- El número total de casillas es impar: no puede existir un recorrido entre los extremos de colores opuestos.
- Un punto de control no tiene el color compatible con su paso.
- Un punto de control está demasiado lejos para llegar a tiempo.
- Dos controles exigen visitar la misma casilla en tiempos diferentes.
- Un control coincide con el destino antes del último paso.
- El robot llega a `(0, 1)` antes de visitar todas las casillas.
- El camino divide las casillas restantes en regiones separadas.
- Se forma una casilla aislada que todavía no fue visitada.
- No existe ninguna solución: se imprime `0`.

## 17. Errores comunes

- Considerar que el inicio es el paso `0`; en el ejemplo, el inicio cuenta como paso `1`.
- Usar división decimal en vez de división entera.
- Permitir movimientos diagonales.
- Permitir regresar a una casilla ya visitada.
- Visitar un punto de control antes de su tiempo.
- Llegar al destino antes del último paso.
- Contar caminos que no visitaron todas las casillas.
- Usar únicamente DFS sin podas, lo que hace la búsqueda demasiado lenta.
- Aplicar una poda intuitiva sin demostrar que es segura y eliminar soluciones válidas.

## 18. Resumen de la decisión

La solución recomendada utiliza:

1. **DFS con backtracking** para construir cada recorrido posible.
2. **Una estructura de visitados** para no repetir casillas.
3. **Metas temporales** para respetar los tres puntos de control y el destino.
4. **Distancia Manhattan y paridad** para descartar metas inalcanzables.
5. **BFS de conectividad** para detectar regiones separadas.
6. **Detección de callejones sin salida** para no encerrar casillas.

El problema es exponencial por naturaleza, pero estas podas hacen que la búsqueda sea mucho más pequeña y permiten resolver las cuadrículas indicadas en el enunciado.
