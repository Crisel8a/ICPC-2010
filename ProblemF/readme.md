<h1 align="center">
  <a href="#">
    Problem F
  </a>
</h1>

<p align="center">
  <strong>Irrigation Channel</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>


## Contexto

Farmer Joe compró una granja para retirarse y criar vacas, pero su terreno está en una región fría y seca. Para poder cultivar, quiere desviar agua de un río y construir un canal de irrigación que serpentee por el campo.

Como las plantas cercanas al canal crecerán mejor, Joe quiere que el canal sea lo más largo posible.

## Representación del campo

El campo es una cuadrícula de `r` filas y `c` columnas.

- `.` representa tierra libre.
- `#` representa una roca inamovible.
- `C` representará el canal en la salida.

## Reglas del canal

El canal:

1. Tiene una celda de ancho.
2. Comienza en la esquina superior izquierda `(0, 0)`.
3. Termina en la esquina inferior derecha `(r - 1, c - 1)`.
4. Solo puede pasar por tierra libre.
5. Está formado por celdas consecutivas que comparten un lado.
6. Debe formar un único camino, sin bifurcaciones.
7. No puede tocarse a sí mismo, ni siquiera diagonalmente por una esquina.

Dos celdas consecutivas pueden tocarse por un lado:

```text
CC
```

Pero dos secciones no consecutivas no pueden tocarse diagonalmente:

```text
C.
.C
```

Ese contacto permitiría que el agua tomara un atajo.

## Objetivo

Encontrar la colocación válida que maximice la cantidad de celdas ocupadas por el canal.

La longitud es el número de caracteres `C` de la solución. El enunciado garantiza que siempre existe una única solución óptima.

---

## Formato de entrada

La entrada contiene varios casos. Cada uno comienza con:

```text
r c
```

Restricciones:

```text
2 ≤ r ≤ 20
2 ≤ c ≤ 9
```

Después aparecen `r` cadenas de longitud `c`, formadas por `.` y `#`.

La entrada termina con:

```text
0 0
```

## Formato de salida

Para cada caso se imprime:

```text
Case k:
```

Después se muestran las `r` filas resultantes:

- Las rocas permanecen como `#`.
- El canal se representa con `C`.
- La tierra no utilizada permanece como `.`.

Debe imprimirse una línea vacía después de cada caso.

## Ejemplo

### Entrada

```text
3 3
.#.
...
.#.
6 7
.......
.......
.......
....#..
.......
.#.....
0 0
```

### Salida

```text
Case 1:
C#.
CCC
.#C

Case 2:
CCCCCCC
......C
CCCCCCC
C...#..
CCC.CCC
.#CCC.C

```

---

## Dificultad principal

El tablero puede tener hasta:

```text
20 × 9 = 180 celdas
```

Una búsqueda que pruebe todos los caminos simples puede ser exponencial en `180`. Guardar el conjunto completo de celdas visitadas también produciría demasiados estados.

La restricción decisiva es:

```text
c ≤ 9
```

La cuadrícula puede ser alta, pero siempre es estrecha. Esto permite usar **programación dinámica de perfil**, también llamada **frontier DP** o **plug DP**.

---

## Decisión de la solución

Procesamos las celdas de izquierda a derecha y de arriba hacia abajo. Solo conservamos información sobre la frontera entre la parte ya procesada y la parte pendiente.

La frontera contiene como máximo una posición por columna, es decir, como máximo `9` posiciones.

Cada estado debe recordar:

1. Qué posiciones de la frontera contienen canal.
2. El grado actual de cada posición.
3. La componente conectada a la que pertenece cada posición.
4. Si la celda diagonal superior izquierda estaba ocupada.
5. La mejor longitud conseguida.
6. Una máscara con las celdas elegidas para reconstruir la salida.

---

## Grados del camino

En un camino válido:

- La esquina superior izquierda tiene grado `1`.
- La esquina inferior derecha tiene grado `1`.
- Cualquier otra celda del canal tiene grado `2`.

El grado es el número de vecinos ortogonales que también pertenecen al canal.

Guardar el grado parcial permite descartar inmediatamente:

- Bifurcaciones de grado `3` o superior.
- Extremos adicionales.
- Celdas internas que nunca podrán completar sus dos conexiones.

---

## Componentes conectadas

Los grados no son suficientes. Podría existir un camino entre las esquinas y, además, un ciclo separado.

Cada posición activa de la frontera guarda una etiqueta de componente.

- Si una celda une dos componentes diferentes, sus etiquetas se fusionan.
- Si une dos puntos que ya pertenecen a la misma componente, crearía un ciclo y el estado se descarta.
- Si una componente desaparece de la frontera antes del final, ya no podrá conectarse con celdas futuras y también se descarta.

Las etiquetas se normalizan para que estados equivalentes tengan la misma clave. Por ejemplo:

```text
5, 5, 8  →  1, 1, 2
```

---

## Representación del estado

Cada posición de la frontera está vacía o contiene:

```text
(etiqueta_de_componente, grado_actual)
```

La frontera se guarda como una tupla inmutable para usarla como clave de un diccionario.

El estado también incluye un bit temporal que indica si la celda superior izquierda de la posición actual contenía canal. Ese dato es necesario para detectar contactos diagonales.

---

## Transición por celda

Para cada celda intentamos como máximo dos decisiones.

### No colocar canal

La posición correspondiente queda vacía. Antes de olvidar la celda superior se comprueba:

- Que su grado final sea correcto.
- Que su componente no desaparezca prematuramente.

### Colocar canal

La celda se conecta automáticamente con las celdas seleccionadas que estén:

- Arriba.
- A la izquierda.

Antes de aceptar la transición se verifica:

1. La celda no es una roca.
2. No toca diagonalmente una sección anterior.
3. Ningún grado supera `2`.
4. Las dos esquinas no superan grado `1`.
5. No se cierra un ciclo.
6. No se pierde una componente incompleta.

Si la transición es válida, la longitud aumenta en uno.

La entrada y la salida son obligatorias: nunca se permite dejarlas vacías.

---

## Contacto diagonal

Al procesar `(fila, columna)`, una nueva celda de canal no puede tener canal en:

```text
(fila - 1, columna - 1)
(fila - 1, columna + 1)
```

La celda superior derecha todavía está en la frontera. La superior izquierda acaba de salir, así que conservamos temporalmente un bit con su ocupación.

Los contactos diagonales hacia abajo se detectarán cuando esas celdas sean procesadas.

---

## Validación al olvidar una celda

Cuando una celda sale de la frontera, ya conocemos todos sus vecinos posibles y su grado no podrá cambiar.

Debe cumplirse:

```text
grado = 1 para la entrada y la salida
grado = 2 para cualquier otra celda del canal
```

Si no se cumple, eliminamos el estado. Esta validación temprana reduce significativamente la cantidad de configuraciones guardadas.

---

## Estado final válido

Después de procesar el tablero completo, solo aceptamos estados donde:

1. Las dos esquinas fueron seleccionadas.
2. Ambas tienen grado `1`.
3. Las demás celdas seleccionadas tienen grado `2`.
4. Todas pertenecen a una única componente.
5. No existe ningún ciclo.
6. No existe contacto diagonal.

Entre ellos elegimos el de mayor longitud.

---

## Reconstrucción

La salida requiere la ubicación exacta, no solo la longitud.

Como existen como máximo `180` celdas, usamos un entero de Python como bitmask:

```text
bit (fila × c + columna) = 1
```

cuando la celda pertenece al canal.

Para cada estado guardamos:

```text
(mejor_longitud, máscara_del_canal)
```

Si dos recorridos producen el mismo estado, conservamos el más largo. La solución óptima global es única, por lo que una sola máscara final determina el tablero.

---

## Pseudocódigo

```text
DP = {estado vacío: (0, máscara 0)}

para cada celda, en orden fila por fila:
    siguiente = diccionario vacío

    para cada estado de DP:
        intentar dejar la celda vacía
        validar grados y componentes olvidadas
        guardar el mejor resultado

        si la celda puede contener canal:
            comprobar diagonales
            conectar con arriba e izquierda
            actualizar grados
            fusionar componentes
            rechazar ciclos y bifurcaciones
            validar la celda olvidada
            sumar uno a la longitud
            activar su bit en la máscara
            guardar el mejor resultado

    DP = siguiente

validar los estados finales
elegir el de mayor longitud
imprimir la máscara elegida
```

---

## Estructuras de datos

### Diccionario

Usamos:

```text
estado → (longitud, máscara)
```

El diccionario solo almacena estados alcanzables, combina estados equivalentes y ofrece actualizaciones `O(1)` promedio.

### Tuplas

La frontera y sus entradas se representan con tuplas inmutables, apropiadas como claves del diccionario.

### Etiquetas normalizadas

Las componentes se renumeran de izquierda a derecha con enteros pequeños para evitar múltiples representaciones de la misma conectividad.

### Entero como máscara

Los enteros de Python tienen precisión arbitraria, así que una máscara de `180` bits funciona sin estructuras adicionales.

---

## ¿Por qué Python?

Python es adecuado porque:

1. La frontera tiene como máximo `9` posiciones.
2. Los diccionarios manejan naturalmente estados dispersos.
3. Las tuplas permiten claves inmutables y claras.
4. Los enteros admiten máscaras mayores de `64` bits.
5. El código de normalización y fusión resulta más legible.

Para mantener el rendimiento:

- Solo conservamos dos capas de DP.
- Normalizamos todas las etiquetas.
- Descartamos estados inválidos inmediatamente.
- Evitamos copiar el tablero completo para cada estado.

---

## Complejidad

Sea `S` el número máximo de estados de frontera válidos en una posición.

`S` es exponencial en la anchura `c`, no en las `r × c` celdas. Como `c ≤ 9`, resulta manejable.

### Tiempo

Procesamos `r × c` celdas, dos decisiones por estado y hasta `c` posiciones al normalizar etiquetas:

```text
O(r × c × S × c)
```

Como `c ≤ 9`, en la práctica se considera:

```text
O(r × c × S)
```

### Memoria

Solo guardamos la capa actual y la siguiente:

```text
O(S × c)
```

Cada valor también contiene una máscara de hasta `r × c` bits.

---

## Argumento de corrección

### El estado es suficiente

Las decisiones futuras solo pueden interactuar con el pasado mediante la frontera. Los grados, componentes y datos diagonales describen completamente esas interacciones.

### La DP genera todas las soluciones válidas

Para cada celda se prueban las dos decisiones posibles. Solo se descartan estados que ya violan una regla o que no podrán conectarse en el futuro.

### La DP rechaza toda solución inválida

- Los grados evitan bifurcaciones y extremos adicionales.
- Las componentes evitan ciclos y fragmentos aislados.
- La comprobación diagonal evita el contacto por esquinas.
- Las rocas nunca se seleccionan.

Por tanto, los estados finales representan exactamente los canales válidos. Elegir el de mayor longitud produce la solución óptima.

---

## Casos especiales

La solución contempla:

- Rocas cerca de la entrada o salida.
- Campos sin rocas.
- Caminos con muchos cambios de dirección.
- Componentes que quedarían aisladas.
- Ciclos parciales.
- Contactos diagonales con una sección antigua.
- El formato con una línea vacía después de cada caso.

## Resumen

Una búsqueda directa es demasiado costosa para `180` celdas. La anchura máxima de `9` permite procesar el campo mediante una DP de frontera.

Los grados garantizan que el canal sea un camino, las etiquetas garantizan la conectividad, la comprobación diagonal impide atajos y una máscara de bits permite reconstruir la única solución óptima.
