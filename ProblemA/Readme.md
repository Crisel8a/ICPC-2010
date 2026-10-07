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

# Problema
Se debe escribir un programa que entienda y ejecute expresiones APL.

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
