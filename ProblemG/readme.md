<h1 align="center">
  <a href="#">
    Problem G
  </a>
</h1>

<p align="center">
  <strong>Shortest Path in Two Passes</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>


## Contexto

Wen Chen es el capitán de un bote de rescate. Todos los días debe visitar un conjunto de islas para comprobar que todo se encuentre en orden.

El capitán comienza en la isla situada más al oeste, realiza una primera pasada hacia la isla más oriental y después regresa hacia el oeste en una segunda pasada hasta la isla inicial.

Durante la primera pasada siempre avanza hacia el este. Durante la segunda siempre avanza hacia el oeste. Puede desplazarse tanto al norte o al sur como sea necesario.

---

## Islas especiales

Existen dos islas especiales, `b₁` y `b₂`, donde el capitán puede obtener combustible.

Estas dos islas deben visitarse en pasadas diferentes:

- Una durante el viaje hacia el este.
- La otra durante el viaje de regreso hacia el oeste.

Como intercambiar las dos pasadas no cambia la longitud geométrica del recorrido, utilizaremos la orientación canónica:

```text
b₁ se visita en la primera pasada
b₂ se visita en la segunda pasada
```

Esto coincide con el formato de los ejemplos y elimina la ambigüedad producida por recorrer el mismo tour en sentido contrario.

---

## Objetivo

Encontrar la ruta de longitud mínima que:

1. Comience en la isla `0`.
2. Avance constantemente hacia el este hasta la isla `n - 1`.
3. Regrese constantemente hacia el oeste hasta la isla `0`.
4. Visite todas las islas exactamente una vez, excepto la isla `0`, que aparece al principio y al final.
5. Visite las dos islas especiales en pasadas diferentes.

Además de la longitud mínima, se debe imprimir el orden exacto de visita.

El problema garantiza que cada caso tiene una solución única.

---

## Orden de las islas

Las islas están numeradas desde `0` hasta `n - 1` y ya aparecen ordenadas de oeste a este:

```text
x₀ < x₁ < x₂ < ... < xₙ₋₁
```

No existen dos islas con la misma coordenada `x`.

Por tanto:

- En la primera pasada los índices visitados aumentan.
- En la segunda pasada los índices disminuyen.

---

## Distancia

La distancia entre dos islas `i` y `j` es euclidiana:

```text
distance(i, j) = √((xᵢ - xⱼ)² + (yᵢ - yⱼ)²)
```

La longitud total es la suma de las distancias entre islas consecutivas del recorrido.

---

## Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con:

```text
n b₁ b₂
```

Donde:

- `n` es el número de islas.
- `b₁` y `b₂` son las islas especiales.

Restricciones:

```text
4 ≤ n ≤ 100
0 < b₁, b₂ < n - 1
b₁ ≠ b₂
```

Después aparecen `n` líneas con:

```text
x y
```

Las coordenadas cumplen:

```text
0 ≤ x, y ≤ 2000
```

Las líneas describen las islas en orden desde la más occidental hasta la más oriental.

La entrada termina con:

```text
0 0 0
```

---

## Formato de salida

Para cada caso se imprimen dos líneas.

La primera contiene:

```text
Case k: longitud
```

La longitud se muestra redondeada al centésimo más cercano, con exactamente dos decimales.

La segunda línea contiene los índices de las islas en el orden de visita, separados por espacios. Debe comenzar y terminar con `0`.

---

## Ejemplo

### Entrada

```text
5 1 3
1 3
3 4
4 1
7 5
8 3
5 3 2
0 10
3 14
4 7
7 10
8 12
0 0 0
```

### Salida

```text
Case 1: 18.18
0 1 4 3 2 0
Case 2: 24.30
0 1 3 4 2 0
```

---

## Interpretación como dos caminos

Un tour válido puede dividirse en dos caminos monotónicos:

```text
Camino A: isla 0 → ... → isla n - 1
Camino B: isla 0 → ... → isla n - 1
```

Ambos avanzan de oeste a este cuando se representan de esta manera.

El tour real se obtiene recorriendo:

1. El camino `A` desde `0` hasta `n - 1`.
2. El camino `B` en sentido inverso, desde `n - 1` hasta `0`.

Cada isla intermedia pertenece exactamente a uno de los dos caminos.

Para fijar la orientación:

```text
b₁ pertenece a A
b₂ pertenece a B
```

Así, el problema se convierte en repartir las islas intermedias entre dos caminos crecientes minimizando la suma de sus longitudes.

---

## Dificultad de una búsqueda directa

Cada una de las `n - 2` islas intermedias podría asignarse al camino `A` o al camino `B`.

Una enumeración completa necesitaría revisar hasta:

```text
2ⁿ⁻²
```

asignaciones. Para `n = 100`, esto es imposible.

La estructura monotónica permite resolver el problema mediante programación dinámica en `O(n²)`.

---

## Decisión de la solución

Utilizaremos una variante de la programación dinámica clásica del **bitonic TSP**.

Procesamos las islas de izquierda a derecha. En cada momento tenemos dos caminos parciales que comienzan en `0`.

El estado se define como:

```text
dp[i][j]
```

y representa la longitud mínima de dos caminos parciales cuyos extremos actuales son `i` y `j`, después de haber asignado todas las islas desde `0` hasta:

```text
k = max(i, j)
```

Cada isla procesada pertenece exactamente a uno de los dos caminos.

---

## Estado inicial

Antes de asignar islas intermedias, ambos caminos comienzan en la isla `0`:

```text
dp[0][0] = 0
```

No se ha recorrido ninguna distancia.

---

## Transiciones

Supongamos que ya procesamos hasta la isla `k` y la siguiente isla es:

```text
next = k + 1
```

Desde el estado `(i, j)` existen como máximo dos opciones.

### Agregar next al camino A

El nuevo estado es:

```text
(next, j)
```

y el costo agregado es:

```text
distance(i, next)
```

La transición completa es:

```text
dp[next][j] = min(
    dp[next][j],
    dp[i][j] + distance(i, next)
)
```

Esta opción no se permite si `next = b₂`, porque `b₂` debe pertenecer al camino `B`.

### Agregar next al camino B

El nuevo estado es:

```text
(i, next)
```

y el costo agregado es:

```text
distance(j, next)
```

La transición completa es:

```text
dp[i][next] = min(
    dp[i][next],
    dp[i][j] + distance(j, next)
)
```

Esta opción no se permite si `next = b₁`.

---

## Tratamiento de la isla final

La isla `n - 1` pertenece a ambos caminos porque es el punto donde termina la primera pasada y comienza el regreso.

Por eso la DP asigna únicamente las islas:

```text
1, 2, ..., n - 2
```

Si después de procesarlas los extremos son `i` y `j`, cerramos ambos caminos agregando:

```text
distance(i, n - 1) + distance(j, n - 1)
```

La respuesta es el mínimo entre todos los estados finales.

---

## Reconstrucción de la ruta

No basta con calcular la distancia; también debemos imprimir el recorrido.

Para cada estado guardamos:

```text
parent[state] = (estado_anterior, camino_elegido)
```

El camino elegido indica si la última isla se añadió a `A` o a `B`.

Después de encontrar el mejor estado final, seguimos los padres hasta `(0, 0)` y reconstruimos la asignación de cada isla.

Obtenemos:

```text
pathA = [0, islas de A en orden, n - 1]
pathB = [0, islas de B en orden, n - 1]
```

El recorrido que se imprime es:

```text
pathA + reverse(pathB sin repetir n - 1)
```

Por ejemplo:

```text
pathA = 0 1 4
pathB = 0 2 3 4
```

produce:

```text
0 1 4 3 2 0
```

---

## Estructuras de datos elegidas

### Lista de coordenadas

Las posiciones se almacenan como:

```text
points[i] = (xᵢ, yᵢ)
```

### Matriz de distancias

Se precomputan las distancias entre todos los pares de islas:

```text
distance[i][j]
```

Esto evita repetir raíces cuadradas durante la DP.

### Diccionario para la capa actual

En cada paso solo existen estados cuyo máximo índice es la última isla procesada. Un diccionario permite almacenar únicamente estados alcanzables:

```text
(i, j) → costo
```

### Diccionario de padres

Guarda la transición óptima que produjo cada estado y permite reconstruir la solución.

---

## ¿Por qué Python?

Python es apropiado porque:

1. `n ≤ 100`, por lo que una DP `O(n²)` es muy pequeña.
2. `math.hypot` calcula distancias euclidianas con claridad.
3. Los diccionarios permiten mantener únicamente estados alcanzables.
4. Las tuplas `(i, j)` son claves naturales para los estados.
5. La reconstrucción mediante padres es directa.

La precisión de `float` es suficiente para coordenadas de hasta `2000` y una ruta de hasta cien islas.

---

## Redondeo

La salida debe mostrar exactamente dos cifras decimales:

```text
18.18
24.30
```

Se utiliza formato decimal con dos posiciones. Puede añadirse una tolerancia pequeña antes del formato para evitar errores binarios mínimos cerca de una frontera de redondeo.

---

## Pseudocódigo

```text
para cada caso:
    leer n, b1, b2
    leer las coordenadas
    precomputar todas las distancias

    current = {(0, 0): 0}
    parent = vacío

    para next desde 1 hasta n - 2:
        following = vacío

        para cada (i, j) en current:
            si next != b2:
                relajar (next, j)
                guardar padre indicando camino A

            si next != b1:
                relajar (i, next)
                guardar padre indicando camino B

        current = following

    elegir (i, j) que minimice:
        current[i, j]
        + distance(i, n - 1)
        + distance(j, n - 1)

    reconstruir las asignaciones siguiendo parent
    construir pathA y pathB
    imprimir pathA seguido de pathB invertido
```

---

## Complejidad

### Tiempo

Precomputar las distancias cuesta:

```text
O(n²)
```

La DP tiene `O(n²)` estados totales y dos transiciones por estado:

```text
O(n²)
```

La reconstrucción cuesta `O(n)`.

Complejidad total:

```text
O(n²)
```

### Memoria

- Matriz de distancias: `O(n²)`.
- Padres de estados: `O(n²)`.
- Capas de la DP: `O(n)` estados por paso.

Memoria total:

```text
O(n²)
```

---

## Argumento de corrección

### Lema 1: todo tour válido corresponde a dos caminos monotónicos

La primera pasada avanza de oeste a este y la segunda de este a oeste. Al invertir la segunda, ambas son caminos crecientes desde `0` hasta `n - 1` y reparten todas las islas intermedias.

### Lema 2: la DP considera todas las asignaciones válidas

Cada isla intermedia se procesa exactamente una vez y se añade a `A` o `B`. Las restricciones de `b₁` y `b₂` eliminan únicamente asignaciones prohibidas.

### Lema 3: cada estado guarda el costo mínimo

Las transiciones agregan exactamente la distancia desde el extremo correspondiente. Mediante relajación, cada par de extremos conserva el menor costo posible.

### Teorema

Todo tour válido aparece como una secuencia de transiciones de la DP y cada secuencia representa un tour válido. Al cerrar ambos caminos en `n - 1` y escoger el costo mínimo, obtenemos la ruta más corta requerida.

---

## Casos especiales

La solución contempla:

- `b₁` situado antes o después de `b₂`.
- Islas especiales cercanas a los extremos.
- Islas con coordenadas verticales muy diferentes.
- Caminos donde una pasada contiene muchas más islas que la otra.
- Distancias finales que requieren redondeo.
- Reconstrucción sin repetir la isla `n - 1`.
- Inicio y final del recorrido en la isla `0`.

## Resumen

El tour se divide en dos caminos monotónicos desde la isla occidental hasta la oriental. Cada isla intermedia se asigna a uno de ellos.

Una DP con los dos extremos actuales calcula el costo mínimo en `O(n²)`. Los padres permiten reconstruir las dos pasadas y producir el orden exacto de visita.
