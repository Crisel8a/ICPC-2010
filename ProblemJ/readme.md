# Sharing Chocolate

## 1. Contexto del problema

Tenemos una barra rectangular de chocolate formada por piezas rectangulares del mismo tamaño. Queremos repartirla entre varios amigos, pero cada amigo pide una porción con una cantidad exacta de piezas.

La barra solamente puede romperse mediante cortes completos y rectos:

- un corte horizontal, realizado entre dos filas; o
- un corte vertical, realizado entre dos columnas.

Cada corte divide un rectángulo en **exactamente dos rectángulos más pequeños**. Después podemos volver a cortar cualquiera de los rectángulos obtenidos de la misma manera.

Al final:

- cada amigo debe recibir un único rectángulo;
- el área de ese rectángulo debe coincidir con la cantidad solicitada;
- debe utilizarse toda la barra;
- no puede sobrar chocolate.

## 2. Objetivo

Debemos determinar si una barra de dimensiones `x × y` puede dividirse en `n` rectángulos cuyas áreas sean exactamente:

```text
a1, a2, ..., an
```

respetando siempre el tipo de corte permitido.

La respuesta para cada caso es:

- `Yes` si existe alguna secuencia válida de cortes;
- `No` si es imposible realizar la división solicitada.

## 3. ¿Qué cortes están permitidos?

Cada corte debe atravesar por completo el rectángulo que se está cortando.

Por ejemplo, un rectángulo puede dividirse así:

```text
┌────────────┐        ┌──────┬─────┐
│            │        │      │     │
│            │   ->   │      │     │
│            │        │      │     │
└────────────┘        └──────┴─────┘
```

o así:

```text
┌────────────┐        ┌────────────┐
│            │        │            │
│            │   ->   ├────────────┤
│            │        │            │
└────────────┘        └────────────┘
```

No están permitidos:

- cortes diagonales;
- porciones no rectangulares;
- cortes que terminen dentro del rectángulo;
- unir posteriormente dos pedazos separados para un mismo amigo.

Este tipo de partición se conoce como una partición mediante **cortes de guillotina**.

## 4. Ejemplo conceptual

Una barra de `3 × 4` tiene:

```text
3 * 4 = 12 piezas
```

Puede dividirse en cuatro porciones de áreas:

```text
6, 3, 2 y 1
```

porque:

```text
6 + 3 + 2 + 1 = 12
```

y existe una secuencia de tres cortes completos que produce cuatro rectángulos con esas áreas.

Es importante notar que la igualdad de áreas es necesaria, pero no siempre suficiente. Puede ocurrir que la suma sea correcta y, aun así, las formas rectangulares no puedan obtenerse con los cortes permitidos.

## 5. Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con un entero:

```text
n
```

donde:

- `n` es la cantidad de porciones;
- `1 <= n <= 15`.

Después aparecen dos enteros:

```text
x y
```

donde:

- `x` y `y` son las dimensiones de la barra;
- `1 <= x, y <= 100`.

Luego aparecen `n` enteros positivos:

```text
a1 a2 ... an
```

Cada valor representa la cantidad de piezas que debe contener la porción de un amigo.

La entrada termina con:

```text
0
```

El cero no representa un caso de prueba.

## 6. Formato de salida

Para cada caso se imprime:

```text
Case k: Yes
```

si la división es posible, o:

```text
Case k: No
```

si no lo es.

El número de caso comienza en `1`.

## 7. Ejemplo

### Entrada

```text
4
3 4
6 3 2 1
2
3 3
1 5
0
```

### Salida

```text
Case 1: Yes
Case 2: No
```

### Explicación

#### Caso 1

La barra tiene área:

```text
3 * 4 = 12
```

Las porciones solicitadas suman:

```text
6 + 3 + 2 + 1 = 12
```

Además, existe una secuencia válida de cortes rectos que produce las cuatro porciones. La respuesta es `Yes`.

#### Caso 2

La barra tiene área:

```text
3 * 3 = 9
```

Las solicitudes suman:

```text
1 + 5 = 6
```

Sobrarían tres piezas, lo cual no está permitido. La respuesta es `No`.

## 8. Primera observación: las áreas deben coincidir

Antes de intentar cualquier corte debemos comprobar:

```text
a1 + a2 + ... + an == x * y
```

Si la suma es diferente, la respuesta es inmediatamente `No`.

Esta condición elimina muchos casos imposibles, pero no resuelve todo el problema. Aunque las áreas coincidan, todavía debemos verificar que puedan organizarse como rectángulos mediante cortes completos.

## 9. Observación principal: pensar en el primer corte

Supongamos que una división válida contiene más de una porción.

Necesariamente existe un **primer corte**. Ese corte divide:

1. el rectángulo actual en dos rectángulos menores;
2. el conjunto de amigos en dos grupos;
3. cada grupo recibe exactamente uno de los dos rectángulos.

Por tanto, podemos probar:

- todas las formas de separar las solicitudes en dos grupos no vacíos;
- un corte horizontal;
- un corte vertical.

Después resolvemos recursivamente el mismo problema para cada mitad.

Esta propiedad permite usar programación dinámica sobre subconjuntos.

## 10. Representación mediante bitmasks

Como `n <= 15`, un subconjunto de amigos puede representarse con los bits de un entero.

Para `n = 4`:

```text
bit 0 -> amigo 0
bit 1 -> amigo 1
bit 2 -> amigo 2
bit 3 -> amigo 3
```

Por ejemplo:

```text
mask = 0101₂
```

representa el subconjunto formado por los amigos `0` y `2`.

Ventajas:

- comprobar pertenencia es rápido;
- separar un conjunto es sencillo;
- existen como máximo `2^15 = 32768` subconjuntos;
- el bitmask puede usarse como parte de la clave de memoización.

Aunque dos amigos pidan la misma cantidad, se mantienen como elementos diferentes porque ocupan bits diferentes.

## 11. Suma de cada subconjunto

Precalculamos:

```text
area[mask]
```

que contiene la suma de las solicitudes incluidas en `mask`.

Por ejemplo, si las solicitudes son:

```text
[6, 3, 2, 1]
```

y `mask` contiene las porciones `6` y `2`, entonces:

```text
area[mask] = 8
```

Esta tabla evita sumar repetidamente los mismos elementos durante la recursión.

Puede calcularse en `O(2^n)` utilizando el bit menos significativo de cada máscara.

## 12. Estado de la programación dinámica

Definimos el estado:

```text
puede_dividir(mask, lado)
```

Su significado es:

> ¿Es posible dividir un rectángulo entre todas las porciones incluidas en `mask`, si uno de sus lados mide `lado`?

El área total del rectángulo ya está determinada por:

```text
area[mask]
```

Por tanto, el otro lado debe medir:

```text
otro_lado = area[mask] / lado
```

Si `area[mask]` no es divisible entre `lado`, ese rectángulo no tiene dimensiones enteras y el estado es imposible.

No necesitamos guardar ambos lados en el estado: con el área y uno de ellos podemos calcular el otro.

Para reducir estados equivalentes, podemos normalizar la orientación:

```text
lado = min(lado, otro_lado)
```

Un rectángulo `3 × 4` y uno `4 × 3` representan el mismo problema porque pueden rotarse.

## 13. Caso base

Si `mask` contiene una única solicitud, no se necesita hacer ningún corte.

El estado es válido porque el rectángulo actual tiene exactamente el área solicitada para esa porción.

```text
si mask tiene un solo bit:
    retornar True
```

## 14. Transición: probar el primer corte

Enumeramos un subconjunto no vacío `submask` de `mask`. El segundo grupo será:

```text
resto = mask XOR submask
```

Sea:

```text
area_1 = area[submask]
area_2 = area[resto]
```

Si el rectángulo actual mide `ancho × alto`, probamos dos posibilidades.

### Corte horizontal

Ambas partes conservan el mismo ancho.

Para que el primer grupo ocupe una cantidad entera de filas debe cumplirse:

```text
area_1 % ancho == 0
```

Su altura será:

```text
alto_1 = area_1 // ancho
```

El corte es válido si:

```text
0 < alto_1 < alto
```

y ambos subproblemas pueden resolverse:

```text
puede_dividir(submask, ancho)
puede_dividir(resto, ancho)
```

### Corte vertical

Ambas partes conservan la misma altura.

Debe cumplirse:

```text
area_1 % alto == 0
```

El ancho del primer grupo será:

```text
ancho_1 = area_1 // alto
```

El corte es válido si:

```text
0 < ancho_1 < ancho
```

y pueden resolverse:

```text
puede_dividir(submask, ancho_1)
puede_dividir(resto, ancho - ancho_1)
```

Si alguna separación funciona, guardamos `True`. Si ninguna funciona, guardamos `False`.

## 15. Evitar particiones repetidas

Separar un conjunto como:

```text
A | B
```

es equivalente a separarlo como:

```text
B | A
```

Para no probar ambas opciones, exigimos que `submask` contenga un bit fijo de `mask`, por ejemplo su bit menos significativo.

Así cada división en dos grupos se considera una sola vez.

## 16. Memoización

Distintas secuencias de cortes pueden llegar al mismo estado:

```text
(mask, lado)
```

Sin memoización, ese estado se resolvería muchas veces.

Guardamos cada resultado:

```text
memo[(mask, lado)] = True o False
```

Cuando el mismo estado vuelve a aparecer, reutilizamos la respuesta inmediatamente.

En Python puede utilizarse:

```python
@lru_cache(None)
```

## 17. Algoritmo paso a paso

1. Leer `n`, las dimensiones y las solicitudes.
2. Calcular el área total de la barra.
3. Si la suma de las solicitudes es diferente, responder `No`.
4. Crear la tabla `area[mask]` para todos los subconjuntos.
5. Llamar a la función memoizada con todos los amigos y uno de los lados de la barra.
6. En cada estado:
   - calcular el segundo lado;
   - retornar `True` si solo queda una porción;
   - enumerar las separaciones del conjunto en dos grupos;
   - probar un corte horizontal;
   - probar un corte vertical.
7. Si algún primer corte produce dos subproblemas válidos, retornar `True`.
8. Si ninguna opción funciona, retornar `False`.
9. Imprimir `Yes` o `No`.

## 18. Ejemplo simplificado de la recursión

Para las solicitudes:

```text
[6, 3, 2, 1]
```

en una barra `3 × 4`, una posibilidad es separar primero:

```text
{6, 3} | {2, 1}
```

Las áreas son:

```text
9 | 3
```

Un corte vertical u horizontal solo será posible si esas áreas corresponden a dimensiones enteras que ocupen completamente ambos lados del corte.

La recursión prueba esta separación y todas las demás separaciones únicas. Cuando encuentra una cuyos dos subproblemas son posibles, concluye que la barra completa también puede dividirse.

La secuencia exacta encontrada por el algoritmo puede usar otra primera separación; lo importante es que se prueban todas las posibilidades válidas.

## 19. Demostración de correctitud

### Lema 1: cada estado describe exactamente un rectángulo

El conjunto `mask` determina el área total requerida. Al conocer uno de los lados, el otro queda determinado por la división del área. Si la división no es exacta, ese rectángulo no puede existir con piezas enteras.

### Lema 2: toda división válida con más de una porción tiene un primer corte

Los únicos cortes permitidos dividen un rectángulo completo en dos rectángulos. Por tanto, cualquier solución con varias porciones comienza con un corte horizontal o vertical que separa las solicitudes en dos grupos no vacíos.

### Lema 3: la transición considera todos los primeros cortes posibles

El algoritmo enumera todos los subconjuntos propios de `mask`, por lo que considera todas las maneras de dividir las solicitudes en dos grupos. Para cada separación prueba las dos orientaciones del corte y verifica que las dimensiones sean enteras.

### Lema 4: si el algoritmo retorna `True`, existe una división válida

El caso base corresponde a entregar un rectángulo completo a un amigo. En un estado mayor, el algoritmo solo retorna `True` cuando encuentra un corte geométricamente válido y ambos rectángulos resultantes pueden dividirse recursivamente. Al unir esos cortes obtenemos una división válida del rectángulo original.

### Lema 5: si existe una división válida, el algoritmo retorna `True`

Tomemos el primer corte de una solución. Ese corte separa las solicitudes en dos grupos que el algoritmo enumerará. También probará su orientación. Por inducción, reconocerá como válidas las divisiones internas de ambas partes y retornará `True`.

### Conclusión

El algoritmo retorna `Yes` si y solo si la barra puede dividirse mediante los cortes permitidos en todas las porciones solicitadas.

## 20. Complejidad

Sea:

- `n` la cantidad de porciones, con `n <= 15`;
- `D` la cantidad de posibles valores para el lado almacenado, con `D <= 100` dentro de la barra original.

### Tiempo

Hay como máximo:

```text
O(2^n * D)
```

estados memoizados.

En cada estado se enumeran subconjuntos. Sumando esta enumeración sobre todas las máscaras se obtiene una cota exponencial del orden de:

```text
O(D * 3^n)
```

En la práctica se exploran muchos menos estados gracias a:

- la comprobación inicial de áreas;
- la divisibilidad de las dimensiones;
- la eliminación de particiones simétricas;
- la memoización;
- el límite `n <= 15`.

### Memoria

La tabla de áreas usa:

```text
O(2^n)
```

La memoización puede almacenar:

```text
O(2^n * D)
```

estados.

La profundidad recursiva es como máximo `n` porque cada corte reduce la cantidad de porciones de los subproblemas.

## 21. ¿Por qué Python?

Python es una buena opción para explicar e implementar esta solución porque ofrece:

- enteros con operaciones de bits sencillas;
- `bit_count()` para saber cuántos elementos tiene una máscara;
- `lru_cache` para memoización automática;
- listas cómodas para precalcular las áreas;
- código recursivo compacto y legible.

Con `n <= 15`, la combinación de bitmasks, poda y memoización mantiene el espacio de búsqueda dentro de límites razonables.

C++ puede ser más rápido en términos absolutos, pero Python permite expresar la misma idea algorítmica de manera clara y conserva una complejidad adecuada para las restricciones.

## 22. Casos especiales

- `n = 1`: solo es posible si la solicitud ocupa toda la barra.
- La suma de solicitudes es menor que el área: sobra chocolate y la respuesta es `No`.
- La suma es mayor que el área: falta chocolate y la respuesta es `No`.
- Dos o más amigos pueden pedir la misma cantidad; cada solicitud sigue siendo independiente.
- Una porción de área válida puede no caber con dimensiones enteras en el rectángulo disponible.
- Rotar un rectángulo no cambia la posibilidad de dividirlo.
- La suma de áreas puede ser correcta y aun así no existir una secuencia válida de cortes de guillotina.

## 23. Errores comunes

- Comprobar únicamente que las áreas sumen lo mismo.
- Permitir porciones no rectangulares.
- Permitir cortes parciales o en forma de `L`.
- Pensar que cualquier partición geométrica puede lograrse con cortes completos.
- Usar una permutación de todas las solicitudes en lugar de subconjuntos.
- No memoizar y repetir los mismos subproblemas.
- Guardar ambos lados sin normalizar y duplicar estados rotados.
- Probar `A | B` y `B | A` como si fueran separaciones diferentes.
- Confundir la cantidad solicitada con una dimensión; representa el **área** de la porción.

## 24. Resumen de la solución

La solución combina:

1. **Comprobación de área total** para descartar casos inmediatos.
2. **Bitmasks** para representar grupos de solicitudes.
3. **Suma precalculada por subconjunto** para conocer el área de cada grupo.
4. **Recursión sobre el primer corte** para probar divisiones horizontales y verticales.
5. **Memoización** para resolver cada estado una sola vez.
6. **Eliminación de simetrías** para evitar trabajo duplicado.

La idea clave es que cualquier solución válida tiene un primer corte. Al probar todas las formas posibles de realizar ese corte y resolver recursivamente sus dos partes, el algoritmo cubre exactamente todas las divisiones permitidas.
