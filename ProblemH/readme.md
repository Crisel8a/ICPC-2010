# Lakes in a Triangulated Landscape

## 1. Contexto del problema

Un paisaje montañoso puede representarse mediante una **triangulación**: un conjunto de puntos con coordenadas y altura, unidos por lados que forman triángulos.

Cuando llueve:

- parte del agua llega al borde del terreno y sale hacia el exterior;
- otra parte queda atrapada en depresiones y forma lagos;
- la lluvia es suficiente para llenar cada lago hasta el nivel máximo que puede alcanzar antes de desbordarse.

El objetivo es encontrar el **nivel final de cada lago**.

## 2. ¿Qué representa cada punto?

Cada punto del terreno contiene:

- un código único de dos caracteres;
- una coordenada horizontal `x`;
- una coordenada horizontal `y`;
- una altura `h` sobre el nivel del mar.

Entre dos puntos conectados por un lado, la altura cambia linealmente. Lo mismo ocurre dentro de cada triángulo. Por tanto, el terreno es una superficie continua formada por planos triangulares.

## 3. Reglas importantes

### El agua que alcanza el borde desaparece

Se considera que el exterior de la región es más bajo que su borde. Por eso, cualquier agua que llegue a un punto del borde puede salir libremente y no forma un lago.

### Los lagos se llenan al máximo

Una depresión acumula agua hasta alcanzar su punto de salida más bajo. La altura de ese punto es el nivel final del lago.

### Un contacto de profundidad cero no une dos lagos

Dos zonas de agua pertenecen al mismo lago solamente si se puede navegar entre ellas por agua de profundidad positiva.

Si dos depresiones se encuentran exactamente en un punto o paso cuya altura coincide con el nivel del agua, en ese lugar la profundidad es cero. En ese caso siguen siendo **dos lagos diferentes**, aunque ambos tengan el mismo nivel.

Por esta razón, la salida puede contener niveles repetidos.

## 4. Objetivo

Para cada caso de prueba debemos:

1. determinar cuántos lagos se forman;
2. calcular el nivel máximo de cada lago;
3. ordenar los niveles de menor a mayor;
4. imprimir `0` si no se forma ningún lago.

## 5. Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con:

```text
p s
```

donde:

- `p` es la cantidad de puntos del terreno, con `p >= 3`;
- `s` es la cantidad de lados de la triangulación, con `s >= 3`.

Después aparecen `p` líneas con el formato:

```text
codigo x y h
```

Restricciones:

- `codigo` tiene dos caracteres y es único dentro del caso;
- `-10000 <= x, y <= 10000`;
- `0 <= h <= 8848`.

A continuación aparecen `s` líneas:

```text
codigo_1 codigo_2
```

Cada línea indica un lado que conecta dos puntos diferentes.

La triangulación cumple que:

- dos lados no se cruzan, excepto en sus extremos;
- toda la región es conexa;
- la región no tiene agujeros;
- su borde es una única curva poligonal cerrada.

La entrada termina con:

```text
0 0
```

Esta línea no representa un caso de prueba.

## 6. Formato de salida

Para cada caso se imprime:

```text
Case k:
  nivel_1
  nivel_2
  ...
```

Los niveles deben aparecer en orden no decreciente. Si no existe ningún lago:

```text
Case k:
  0
```

## 7. Ejemplo

### Entrada

```text
3 3
AA 0 0 0
BB 0 1 0
CC 1 0 0
AA BB
AA CC
BB CC
7 12
aa 1 1 5
bb 1 3 5
xX 0 2 10
XY 0 4 15
XZ 3 4 11
xy 0 0 15
xz 3 0 15
xX XZ
XY XZ
xX XY
xX xy
xX xz
xz xy
aa xX
aa xy
aa xz
bb xX
bb XY
bb XZ
0 0
```

### Salida

```text
Case 1:
  0
Case 2:
  10
  10
```

### Explicación del ejemplo

- En el primer caso, los tres puntos pertenecen al borde. El agua puede salir y no se forma ningún lago.
- En el segundo caso hay dos depresiones diferentes.
- Ambas se llenan hasta la altura `10`.
- Solo se tocan donde la profundidad es cero, así que se cuentan como dos lagos distintos.

## 8. Observación principal

Podemos imaginar que el nivel del agua sube desde las alturas más bajas hacia las más altas.

Para una altura `H`, los puntos situados por debajo de `H` forman componentes conectados:

- una componente que ya está conectada con el borde **drena**;
- una componente que no está conectada con el borde es una **depresión atrapada**.

Cuando una depresión atrapada se conecta por primera vez con una componente que drena, encontramos su nivel de desbordamiento. Si esto sucede a la altura `H`, existe un lago cuyo nivel final es `H`.

La conectividad de las zonas inferiores solo puede cambiar al alcanzar la altura de algún vértice. Por eso basta procesar los vértices ordenados por `h`; no es necesario simular cada posible nivel del agua.

## 9. Estructuras de datos elegidas

### Diccionario de códigos

Se utiliza un diccionario de Python:

```text
codigo -> indice numerico
```

Esto permite convertir códigos como `AA` o `xX` en índices enteros y trabajar cómodamente con listas.

### Lista de adyacencia

Para cada punto guardamos sus vecinos. Esta representación permite:

- recorrer los lados del terreno;
- ordenar los vecinos geométricamente;
- encontrar qué componentes participan en cada evento de altura.

### Union-Find o DSU

La estructura principal es **Disjoint Set Union**, también llamada **Union-Find**.

Permite:

- saber rápidamente a qué componente pertenece un punto;
- unir dos componentes cuando el nivel del agua alcanza el lado que las conecta;
- guardar si una componente está conectada con el borde.

Sus operaciones principales son:

- `find(x)`: obtiene el representante de la componente de `x`;
- `union(a, b)`: une las componentes de `a` y `b`.

Con compresión de caminos y unión por tamaño, ambas operaciones tienen un coste amortizado prácticamente constante.

### Componentes temporales por altura

Todos los vértices con la misma altura deben procesarse juntos. Para ello se construye, en cada altura, un pequeño grafo temporal compuesto por:

- los nuevos vértices de esa altura;
- las componentes de alturas menores que son vecinas de esos vértices.

Este grafo permite decidir correctamente qué depresiones se encuentran o desbordan en el mismo nivel.

## 10. ¿Cómo se detecta el borde?

El enunciado no indica directamente cuáles son los puntos del borde, así que debemos obtenerlos a partir de las coordenadas y los lados.

Se usan los lados como **semilados dirigidos**:

- cada lado no dirigido `u - v` produce `u -> v` y `v -> u`;
- en cada punto, sus vecinos se ordenan por su ángulo alrededor del punto;
- desde un semilado `u -> v`, se continúa por el semilado que mantiene la misma cara a la izquierda.

De esta manera se recorren todas las caras del dibujo plano.

- Las caras interiores son los triángulos.
- La cara exterior se recorre con la orientación contraria y tiene área firmada negativa.
- Todos los puntos encontrados en esa cara exterior son puntos del borde.

Esto es más seguro que usar la envolvente convexa, porque el borde de la región puede ser cóncavo.

## 11. Algoritmo paso a paso

### Paso 1: leer el terreno

Guardamos:

- código, coordenadas y altura de cada punto;
- todos los lados;
- la lista de vecinos de cada punto.

### Paso 2: encontrar la cara exterior

Ordenamos los vecinos de cada punto por ángulo y recorremos las caras mediante semilados dirigidos. Los vértices de la cara exterior se marcan como puntos de drenaje.

### Paso 3: ordenar los puntos por altura

Los puntos se agrupan por su altura `h` y las alturas se procesan en orden creciente.

### Paso 4: analizar simultáneamente una altura `H`

Antes de activar los nuevos puntos, el DSU representa únicamente el terreno situado a alturas menores que `H`.

Construimos las componentes temporales que aparecen en el nivel `H`, teniendo en cuenta:

- conexiones entre nuevos puntos de altura `H`;
- conexiones desde esos puntos hacia componentes ya activas de menor altura.

### Paso 5: clasificar cada evento

Para cada componente temporal comprobamos si:

- contiene un punto del borde; o
- toca una componente que ya drenaba.

Si ocurre cualquiera de las dos condiciones, el evento está conectado con el exterior.

### Paso 6: registrar los lagos

Si el evento drena, cada componente atrapada de menor altura que llega al evento representa un lago que se llena hasta `H`.

Se agrega `H` una vez por cada una de esas componentes atrapadas diferentes.

No se cuenta como lago una región que nace y drena en la misma altura, porque nunca llega a tener profundidad positiva.

### Paso 7: unir las componentes

Después de analizar el evento, activamos los nuevos puntos y realizamos las uniones definitivas en el DSU.

- Si el evento toca el borde, la nueva componente queda marcada como drenante.
- Si no toca el borde, continúa como una depresión atrapada que podrá crecer o unirse con otra depresión más adelante.

### Paso 8: producir la respuesta

Los niveles encontrados se ordenan de menor a mayor. Si la lista está vacía, se imprime `0`.

## 12. ¿Por qué se procesan juntas las alturas iguales?

Procesar uno por uno los puntos con la misma altura produciría un resultado dependiente del orden de lectura, lo cual sería incorrecto.

Supongamos que dos depresiones alcanzan el mismo paso de salida a altura `H`:

- justo por debajo de `H` todavía son dos componentes diferentes;
- en `H` ambas llegan a una zona por la que el agua drena;
- como solo se tocan con profundidad cero, deben producir dos lagos de nivel `H`.

Si uniéramos la primera depresión con la segunda antes de decidir el drenaje, contaríamos un solo lago. El procesamiento por lotes conserva las componentes existentes **justo antes** de `H` y permite contar ambas correctamente.

## 13. Idea de correctitud

### Lema 1: el DSU representa las regiones inundables ya alcanzadas

Después de procesar todas las alturas menores que `H`, dos puntos activos pertenecen al mismo conjunto exactamente cuando pueden conectarse permaneciendo por debajo de `H`.

Esto se cumple porque cada lado se incorpora cuando sus extremos ya están activos y el terreno es lineal dentro de cada triángulo.

### Lema 2: una componente marcada como drenante no puede formar un lago

Si una componente toca el borde, el agua puede continuar hacia el exterior, que se considera más bajo. Por tanto, esa agua no queda atrapada.

### Lema 3: una componente atrapada que alcanza el drenaje en `H` forma un lago de nivel `H`

Antes de `H` la componente no tenía salida, así que retenía agua. Al alcanzar `H` aparece por primera vez un camino hacia el borde. El agua no puede superar ese nivel porque se derramaría, de modo que su nivel máximo es exactamente `H`.

### Lema 4: el procesamiento por lotes cuenta correctamente los contactos de profundidad cero

Las componentes atrapadas existentes justo por debajo de `H` se mantienen separadas mientras se analiza el evento. Si varias llegan al drenaje en `H`, se registra un lago por cada componente, aunque sus niveles sean iguales.

### Conclusión

El algoritmo registra todos los lagos cuando alcanzan por primera vez una salida, no registra regiones que siempre drenan y respeta la regla de los contactos con profundidad cero. Por tanto, produce exactamente los niveles pedidos.

## 14. Complejidad

Sean:

- `p` la cantidad de puntos;
- `s` la cantidad de lados.

### Tiempo

- Ordenar los puntos por altura: `O(p log p)`.
- Ordenar los vecinos por ángulo para hallar las caras: `O(s log p)` en el peor caso.
- Recorrer caras, lados y eventos: `O((p + s) alpha(p))`.

`alpha(p)` es la función inversa de Ackermann y crece tan lentamente que se considera casi constante.

La complejidad total es:

```text
O((p + s) log p)
```

Como el grafo es una triangulación plana, normalmente `s = O(p)`, por lo que también puede expresarse como:

```text
O(p log p)
```

### Memoria

Se almacenan los puntos, lados, adyacencias y estructuras DSU:

```text
O(p + s)
```

Para una triangulación plana, esto equivale a `O(p)`.

## 15. ¿Por qué Python?

Python es una buena elección para esta solución porque ofrece:

- diccionarios eficientes para convertir códigos en índices;
- listas cómodas para representar el grafo;
- ordenamiento incorporado con `sorted()`;
- una implementación clara de Union-Find;
- enteros sin riesgo de desbordamiento al calcular productos y áreas firmadas.

Aunque lenguajes como C++ suelen ser más rápidos, la solución en Python conserva una complejidad adecuada y permite expresar el algoritmo de forma más sencilla y legible.

## 16. Errores comunes

- Suponer que el borde es la envolvente convexa.
- Procesar por separado vértices que tienen la misma altura.
- Contar como un solo lago dos depresiones que únicamente se tocan con profundidad cero.
- Marcar como lago una región que ya está conectada con el borde.
- Olvidar que pueden existir varios lagos con el mismo nivel.
- Imprimir los niveles sin ordenarlos.
- Procesar `0 0` como si fuera otro caso.

## 17. Resumen de la decisión

La solución combina tres ideas:

1. **Geometría plana** para descubrir el borde real de la región.
2. **Procesamiento ascendente por alturas** para simular cómo se llenan las depresiones.
3. **Union-Find por lotes** para mantener componentes eficientemente y respetar los contactos de profundidad cero.

Esta estrategia evita simular el agua punto por punto y resuelve el problema dentro de una complejidad cercana a `O(p log p)`.
