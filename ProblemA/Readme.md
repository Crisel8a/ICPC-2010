<h1 align="center">
  <a href="#">
    Problem A
  </a>
</h1>

<p align="center">
  <strong>APL Lives!</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>

# ¿Qué es APL?
APL es un lenguaje de programación especializado en trabajar con vectores y matrices.

En lenguajes comunes escribirías:
```c
vector<int> numeros = {1, 2, 3};
```


En APL simplemente:

```c
1 2 3
```

El problema no utiliza todo APL, sino una versión pequeña llamada apl.
# ¿Qué es un intérprete?
Un intérprete es un programa que:

- Recibe código escrito como texto.
- Analiza qué significa.
- Ejecuta las instrucciones.
- Muestra el resultado.
- Por ejemplo, tu programa recibe:

```c
iota 5
```
Debe comprender que iota 5 significa “generar los números del 1 al 5” y producir:

```c
1 2 3 4 5
```

# Input
La entrada contiene varias expresiones. Cada expresión aparece en una línea:


```c
var = 1 2 3
var + 4
iota 5
2 drop iota 5
#
```

La línea:
```c
#
```

indica que la entrada terminó y no debe procesarse. Cada línea anterior a # es un caso diferente.

# Output
Por cada expresión se debe imprimir:

```c
Case número: expresión original
resultado
Para la entrada anterior:
```

```c
var = 1 2 3
var + 4
iota 5
2 drop iota 5
#
```

la salida sería:

```c
Case 1: var = 1 2 3
1 2 3
Case 2: var + 4
5 6 7
Case 3: iota 5
1 2 3 4 5
Case 4: 2 drop iota 5
3 4 5
```

Las variables se conservan entre casos. Por eso var, creada en el caso 1, puede usarse en el caso 2.

## Generación: iota
Genera los números desde 1 hasta el número indicado:

```c
iota 5
```
Resultado:

```c
1 2 3 4 5
```

## Eliminación: drop
Elimina elementos del principio:

```c
2 drop 1 2 3 4 5
```

Resultado:

```c
3 4 5
```

## Cambio de forma: rho
Convierte un vector en una matriz:

```c
2 2 rho 1 2 3 4
```

2 2 indica dos filas y dos columnas:

```c
1 2
3 4
```

Otro ejemplo:

```c
2 3 rho 1 2 3 4
```

Se necesitan seis valores, pero solamente hay cuatro. Por eso vuelve a utilizarlos desde el principio:

```c
1 2 3
4 1 2
```

## Reducción: + /, - /, * /
Inserta un operador entre los elementos.

```c
+ / 1 2 3 4
```

Equivale a:

```c
1 + 2 + 3 + 4
```

Resultado:

```c
10
```
En el caso de la resta se mantiene la evaluación de derecha a izquierda:

```c
- / 1 2 3
```

Equivale a:

```c
1 - (2 - 3)
```

Resultado:

```c
2
```

# Evaluación de derecha a izquierda
** siempre se comienza por la derecha:**

```c
10 - 5 - 2
```

Se interpreta como:

```c
10 - (5 - 2)
```

# Problema
Se debe escribir un programa que entienda y ejecute expresiones APL.

Para cada línea:

- Separar la expresión en elementos.
- Reconocer números, variables, operadores y paréntesis.
- Determinar el orden de las operaciones.
- Evaluarlas de derecha a izquierda.
- Guardar las variables creadas con =.
- Manejar vectores, matrices y arreglos 3D.
- Imprimir el resultado con el formato solicitado.


