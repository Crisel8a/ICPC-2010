<h1 align="center">
  <a href="#">
    Problem F
  </a>
</h1>

<p align="center">
  <strong>Contour Mapping</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>


## Contexto

Un mapa de contorno representa la topografía de una región mediante líneas de elevación constante. Por ejemplo, una línea puede representar todos los puntos situados a `100` metros sobre el nivel del mar y otra los puntos situados a `200` metros.

La **Association for Contour Mapping (ACM)** necesita producir mapas de contorno a partir de mediciones de elevación obtenidas por un satélite.

Las mediciones están organizadas en líneas de exploración de oeste a este. Los puntos están intercalados de manera que cada medición tiene seis vecinos cercanos, ignorando las fronteras del conjunto. Al conectar esos vecinos se forma una malla de triángulos equiláteros.

Cada triángulo se considera una superficie plana cuya elevación cambia linealmente entre sus tres vértices.

---

## Objetivo

Calcular la longitud total de todas las líneas de contorno del mapa.

Las líneas aparecen en elevaciones que son múltiplos enteros de un incremento `h`:

```text
h, 2h, 3h, 4h, ...
```

Una línea puede atravesar el interior de un triángulo o coincidir con una de sus aristas.

El resultado debe redondearse al entero más cercano.

---

## Malla de mediciones

La entrada contiene `s` líneas de exploración.

- Las líneas impares, numeradas desde `1`, contienen `p` mediciones.
- Las líneas pares contienen `p + 1` mediciones.

La distancia entre puntos vecinos es `d`. Al proyectarlos sobre el plano de elevación cero se forma una malla de triángulos equiláteros de lado `d`.

Si numeramos las filas desde cero, podemos asignar las coordenadas:

```text
altura_vertical = d × √3 / 2
```

Para una fila par de índice cero —una línea impar en el enunciado—:

```text
x = d / 2 + columna × d
y = fila × altura_vertical
```

Para una fila impar de índice cero:

```text
x = columna × d
y = fila × altura_vertical
```

La orientación vertical no afecta las longitudes; estas coordenadas solo permiten calcular distancias e interpolaciones.

---

## Triangulación

Entre dos filas consecutivas siempre existe:

- Una fila pequeña con `p` puntos.
- Una fila grande con `p + 1` puntos.

Para cada par de filas se crean:

```text
2p - 1 triángulos
```

La malla completa contiene:

```text
(s - 1)(2p - 1) triángulos
```

Con los límites máximos:

```text
(100 - 1)(2 × 100 - 1) = 19 701 triángulos
```

---

## Superficie dentro de un triángulo

Cada triángulo se trata como una superficie plana determinada por las posiciones y elevaciones de sus tres vértices.

Si una elevación de contorno `L` se encuentra entre la menor y la mayor elevación del triángulo, la intersección del plano horizontal `z = L` con el triángulo es normalmente un segmento recto.

La longitud de ese segmento contribuye a la longitud total del mapa.

---

## Regiones planas

Puede ocurrir que los tres vértices de uno o varios triángulos tengan la misma elevación.

En ese caso no se dibujan infinitas líneas dentro de la región plana. Solo se dibuja su frontera.

Esto requiere un tratamiento especial para las aristas cuyos dos extremos tienen exactamente la misma elevación de contorno.

---

## Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con cuatro enteros:

```text
s p d h
```

Donde:

- `s`: número de líneas de exploración, `2 ≤ s ≤ 100`.
- `p`: mediciones en las líneas impares, `1 ≤ p ≤ 100`.
- `d`: distancia entre puntos vecinos, `1 ≤ d ≤ 10`.
- `h`: incremento entre líneas de contorno, `1 ≤ h ≤ 1000`.

Después aparecen las elevaciones, todas enteras no negativas y no mayores que `10⁶`.

Se proporcionan en este orden:

```text
p valores para la primera línea
p + 1 valores para la segunda
p valores para la tercera
p + 1 valores para la cuarta
...
```

Los saltos de línea y líneas vacías solo separan visualmente los datos. La lectura puede realizarse como una secuencia de enteros.

La entrada termina con una línea que contiene:

```text
0
```

---

## Formato de salida

Para cada caso se imprime:

```text
Case k: longitud
```

Donde:

- `k` es el número del caso, comenzando en `1`.
- `longitud` es la longitud total de todas las líneas de contorno, redondeada al entero más cercano.

---

## Ejemplo

### Entrada

```text
3 2 5 5
1 1
1 9 1
1 1

4 4 5 3
5 7 7 5
5 9 9 9 5
9 9 9 9
7 9 9 9 7

0
```

### Salida

```text
Case 1: 15
Case 2: 54
```

---

## Dificultad principal

Una solución directa podría recorrer, para cada triángulo, todos los múltiplos de `h` entre su elevación mínima y máxima.

Esto no es viable. Las elevaciones pueden llegar a `10⁶`, `h` puede ser `1` y existen casi veinte mil triángulos. El número total de niveles examinados podría ser enorme.

La observación clave es que, dentro de un triángulo plano, la longitud de la intersección con un nivel horizontal cambia linealmente con la elevación.

Por tanto, todas las contribuciones de un intervalo pueden sumarse mediante una serie aritmética, sin visitar cada línea de contorno.

---

## Decisión de la solución

La solución tiene cuatro etapas:

1. Construir los puntos y sus coordenadas.
2. Construir la lista de triángulos y las aristas únicas.
3. Sumar en `O(1)` todos los segmentos interiores de cada triángulo.
4. Agregar por separado las aristas que coinciden con un nivel de contorno.

---

## 1. Construcción geométrica

Cada punto se almacena con:

```text
(x, y, elevación)
```

También se conserva un identificador entero para referenciarlo desde triángulos y aristas.

Para cada par de filas consecutivas identificamos la fila pequeña y la grande.

Se crean dos familias de triángulos:

```text
(small[j], large[j], large[j + 1])
```

para `0 ≤ j < p`, y:

```text
(small[j], small[j + 1], large[j + 1])
```

para `0 ≤ j < p - 1`.

---

## 2. Longitud dentro de un triángulo

Ordenamos los tres vértices por elevación:

```text
z₀ ≤ z₁ ≤ z₂
```

La longitud del segmento de contorno crece linealmente desde la elevación mínima hasta `z₁` y decrece linealmente desde `z₁` hasta la máxima.

Sea `P` la longitud del segmento en la elevación `z₁`.

### Tramo inferior

Para:

```text
z₀ < L ≤ z₁
```

la longitud es:

```text
length(L) = P × (L - z₀) / (z₁ - z₀)
```

### Tramo superior

Para:

```text
z₁ < L < z₂
```

la longitud es:

```text
length(L) = P × (z₂ - L) / (z₂ - z₁)
```

El nivel `z₁` se incluye una sola vez.

---

## Cálculo de P

### Tres elevaciones distintas

Si:

```text
z₀ < z₁ < z₂
```

interpolamos sobre la arista que une los vértices de elevaciones `z₀` y `z₂`.

El parámetro es:

```text
t = (z₁ - z₀) / (z₂ - z₀)
```

El punto interpolado es:

```text
Q = V₀ + t(V₂ - V₀)
```

Entonces:

```text
P = distancia(V₁, Q)
```

### Dos elevaciones mínimas iguales

Si:

```text
z₀ = z₁ < z₂
```

el segmento máximo coincide con la arista entre los dos vértices bajos:

```text
P = d
```

### Dos elevaciones máximas iguales

Si:

```text
z₀ < z₁ = z₂
```

también se cumple:

```text
P = d
```

### Triángulo completamente plano

Si:

```text
z₀ = z₁ = z₂
```

no se agrega área interior. Sus fronteras se procesan mediante las aristas.

---

## 3. Suma de niveles sin iterarlos

Los niveles de contorno tienen la forma:

```text
L = k × h
```

Para todos los múltiplos dentro de un intervalo encontramos:

```text
k_primero
k_último
cantidad = k_último - k_primero + 1
```

La suma de las elevaciones es:

```text
ΣL = h × (k_primero + k_último) × cantidad / 2
```

Por ejemplo, para el tramo inferior necesitamos sumar:

```text
Σ P × (L - z₀) / (z₁ - z₀)
```

Sacando las constantes:

```text
P / (z₁ - z₀) × (ΣL - cantidad × z₀)
```

Así calculamos la contribución de todos los niveles del tramo en tiempo constante.

El tramo superior se calcula de forma análoga:

```text
P / (z₂ - z₁) × (cantidad × z₂ - ΣL)
```

La cantidad de operaciones ya no depende de la diferencia entre elevaciones.

---

## 4. Contornos que coinciden con aristas

Si los dos extremos de una arista tienen la misma elevación y esa elevación es múltiplo de `h`, la línea de contorno puede coincidir con toda la arista.

Estas aristas se procesan por separado para evitar contarlas dos veces desde los triángulos adyacentes.

Cada arista de la malla mide exactamente:

```text
d
```

La arista se agrega una sola vez, excepto cuando es una arista interna de una región completamente plana.

Si una arista tiene dos triángulos adyacentes y ambos son planos con esa misma elevación, la arista está dentro de la región plana y no debe dibujarse.

Si la arista está en la frontera de la región plana, sí se cuenta.

---

## Estructuras de datos elegidas

### Lista de puntos

Cada punto almacena coordenadas y elevación.

### Lista de triángulos

Cada triángulo es una tupla con tres identificadores de puntos.

### Diccionario de aristas

Una arista se representa como:

```text
(min(u, v), max(u, v))
```

El diccionario guarda los triángulos adyacentes a cada arista. Esto permite:

- Evitar duplicados.
- Detectar aristas internas de regiones planas.
- Contar una arista de contorno exactamente una vez.

### Números enteros y flotantes

- Los índices y sumas de niveles se calculan con enteros.
- Las coordenadas, interpolaciones y longitudes usan `float`.

---

## ¿Por qué Python?

Python es adecuado porque:

1. Solo existen alrededor de veinte mil triángulos en el caso máximo.
2. Cada triángulo se procesa en tiempo constante.
3. Los diccionarios facilitan deduplicar aristas.
4. Los enteros de Python evitan desbordamientos en las series aritméticas.
5. `math.sqrt` y `math.hypot` permiten expresar claramente la geometría.

La optimización importante no es usar operaciones de bajo nivel, sino evitar iterar por hasta un millón de niveles en cada triángulo.

---

## Redondeo

La longitud total es no negativa y se acumula como número flotante.

Para redondear al entero más cercano puede utilizarse conceptualmente:

```text
entero = floor(total + 0.5)
```

Puede añadirse una tolerancia pequeña para evitar que errores binarios mínimos cambien un resultado situado exactamente en una frontera de redondeo.

---

## Pseudocódigo

```text
para cada caso:
    leer s, p, d, h
    construir puntos con coordenadas y elevaciones
    construir todos los triángulos
    construir diccionario de aristas y adyacencias

    total = 0

    para cada triángulo:
        ordenar sus vértices por elevación

        si no es completamente plano:
            calcular P
            sumar todos los niveles del tramo inferior en O(1)
            sumar todos los niveles del tramo superior en O(1)

    para cada arista única:
        si sus extremos tienen la misma elevación múltiplo de h:
            si no es interna a una región plana:
                total += d

    imprimir total redondeado
```

---

## Complejidad

Sea:

```text
T = (s - 1)(2p - 1)
```

el número de triángulos.

La cantidad de aristas únicas también es `O(T)`.

### Tiempo

- Construcción de puntos: `O(sp)`.
- Construcción de triángulos: `O(T)`.
- Contribuciones interiores: `O(T)`.
- Procesamiento de aristas: `O(T)`.

Complejidad total:

```text
O(sp)
```

Esta complejidad es independiente del rango de elevaciones y de la cantidad de múltiplos de `h` existentes.

### Memoria

- Puntos: `O(sp)`.
- Triángulos: `O(sp)`.
- Aristas: `O(sp)`.

Memoria total:

```text
O(sp)
```

---

## Argumento de corrección

### Lema 1: cada contorno interior se suma correctamente

Dentro de un triángulo plano, la intersección con un nivel horizontal es un segmento cuya longitud varía linealmente en cada lado de `z₁`. Las fórmulas de los dos tramos calculan exactamente esa longitud.

### Lema 2: la serie aritmética suma todos los niveles

Los niveles válidos son múltiplos consecutivos de `h`. La fórmula de suma incluye cada múltiplo del intervalo exactamente una vez, sin enumerarlos.

### Lema 3: las aristas coincidentes se cuentan una vez

El diccionario contiene cada arista geométrica una sola vez. Se cuentan las aristas que son contornos y se eliminan únicamente las que quedan dentro de una región plana.

### Teorema

Todo fragmento de una línea de contorno está dentro de un triángulo o coincide con una arista. Ambos casos se procesan sin omisiones ni duplicados. Por tanto, la suma obtenida es la longitud total de todas las líneas de contorno.

---

## Casos especiales

La solución contempla:

- Triángulos completamente planos.
- Dos vértices con la misma elevación.
- Un vértice exactamente en un nivel de contorno.
- Contornos que coinciden con aristas.
- Regiones planas formadas por varios triángulos.
- Elevaciones muy separadas con `h = 1`.
- Múltiples contornos dentro de un mismo triángulo.
- Líneas vacías entre casos de prueba.

## Resumen

La malla se divide en triángulos equiláteros y cada uno se interpreta como una superficie plana. La longitud de sus cortes horizontales es lineal por tramos, por lo que todos los niveles múltiples de `h` pueden sumarse con series aritméticas.

Las aristas coincidentes se procesan por separado para manejar correctamente regiones planas y evitar duplicados. El resultado es un algoritmo `O(sp)`, claro y eficiente en Python.
