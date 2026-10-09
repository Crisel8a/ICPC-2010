<h1 align="center">
  <a href="#">
    Problem B
  </a>
</h1>

<p align="center">
  <strong>Barcodes</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>
# Decodificador de códigos de barras Code-11

## Descripción del problema

Code-11 es un sistema de códigos de barras utilizado principalmente para identificar equipos de telecomunicaciones. Puede representar los dígitos del `0` al `9`, el guion `-` y un símbolo especial de inicio y fin llamado **Start/Stop**.

En este problema no se recibe una imagen del código de barras. Un lector ya ha escaneado el código y entrega una secuencia de números con las anchuras de las regiones oscuras y claras detectadas.

El objetivo es reconstruir el mensaje original, comprobar que la estructura del código sea válida y verificar dos caracteres de seguridad llamados `C` y `K`.

---

## Codificación de los caracteres

Cada carácter de Code-11 está formado por cinco regiones consecutivas que alternan entre:

```text
oscura, clara, oscura, clara, oscura
```

Cada región puede ser estrecha o ancha:

- `0`: región estrecha.
- `1`: región ancha.

La tabla de codificación es la siguiente:

| Carácter | Codificación |
|:--------:|:------------:|
| `0` | `00001` |
| `1` | `10001` |
| `2` | `01001` |
| `3` | `11000` |
| `4` | `00101` |
| `5` | `10100` |
| `6` | `01100` |
| `7` | `00011` |
| `8` | `10010` |
| `9` | `10000` |
| `-` | `00100` |
| Start/Stop | `00110` |

Por ejemplo, el carácter `1` se codifica como:

```text
10001
```

Esto representa, en orden:

1. Una región oscura ancha.
2. Una región clara estrecha.
3. Una región oscura estrecha.
4. Una región clara estrecha.
5. Una región oscura ancha.

Entre dos caracteres consecutivos siempre debe existir una región clara estrecha que funciona como separador.

---

## Anchuras de las regiones

Idealmente, una región ancha mide exactamente el doble que una región estrecha:

```text
ancha = 2 × estrecha
```

Sin embargo, la impresión del código puede ser imprecisa. Cada región puede medir hasta un `5%` más o un `5%` menos de su anchura esperada.

Si la anchura ideal de una región estrecha es `w`, entonces:

- Una región estrecha puede medir entre `0.95w` y `1.05w`.
- Una región ancha puede medir entre `1.90w` y `2.10w`.

Todas las medidas recibidas deben poder clasificarse de forma coherente como estrechas o anchas. Si esto no es posible, el código es inválido.

---

## Dirección del escaneo

El código de barras puede haber sido escaneado:

- De izquierda a derecha.
- De derecha a izquierda.

Por lo tanto, la secuencia de anchuras puede aparecer en el orden normal o completamente invertida. El programa debe reconocer ambas orientaciones.

---

## Estructura del código completo

Un código válido tiene la siguiente estructura:

```text
Start | mensaje | C | K | Stop
```

Donde:

- `Start` es el símbolo especial de inicio.
- `mensaje` contiene uno o más caracteres.
- `C` es el primer carácter de verificación.
- `K` es el segundo carácter de verificación.
- `Stop` es el símbolo especial de finalización.

No existen mensajes vacíos. Debe haber al menos un carácter entre `Start` y los caracteres de verificación.

Por ejemplo, si el mensaje es:

```text
123-45
```

sus caracteres de verificación son:

```text
C = 5
K = 2
```

La secuencia completa de caracteres codificados sería:

```text
Start 1 2 3 - 4 5 5 2 Stop
```

Al mostrar el resultado, solamente se imprime el mensaje original. Los caracteres `C`, `K`, `Start` y `Stop` no forman parte del mensaje mostrado.

---

## Peso de los caracteres

Para calcular los caracteres de verificación, cada símbolo tiene un peso numérico:

| Carácter | Peso |
|:--------:|:----:|
| `0` a `9` | `0` a `9` |
| `-` | `10` |

Si un cálculo produce el valor `10`, el carácter correspondiente es `-`.

---

## Carácter de verificación C

Supongamos que el mensaje contiene `n` caracteres:

```text
c₁, c₂, ..., cₙ
```

El peso del carácter `C` se calcula mediante:

```text
C = (Σ ((((n - i) mod 10) + 1) × peso(cᵢ))) mod 11
```

Los multiplicadores se aplican desde la derecha con la secuencia:

```text
1, 2, 3, ..., 10, 1, 2, ...
```

### Ejemplo

Para el mensaje:

```text
123-45
```

los pesos de los caracteres son:

```text
1, 2, 3, 10, 4, 5
```

Los multiplicadores correspondientes son:

```text
6, 5, 4, 3, 2, 1
```

Entonces:

```text
1×6 + 2×5 + 3×4 + 10×3 + 4×2 + 5×1 = 71
71 mod 11 = 5
```

Por tanto:

```text
C = 5
```

---

## Carácter de verificación K

Para calcular `K`, se utilizan los caracteres del mensaje y también el carácter `C` ya calculado.

Si `cₙ₊₁` representa el carácter `C`, entonces:

```text
K = (Σ ((((n - i + 1) mod 9) + 1) × peso(cᵢ))) mod 11
```

La suma se realiza para:

```text
i = 1 hasta n + 1
```

Los multiplicadores se aplican desde la derecha con la secuencia:

```text
1, 2, 3, ..., 9, 1, 2, ...
```

### Ejemplo

Para el mensaje `123-45`, sabemos que `C = 5`. Los caracteres usados para calcular `K` son:

```text
1 2 3 - 4 5 5
```

Sus multiplicadores son:

```text
7, 6, 5, 4, 3, 2, 1
```

Entonces:

```text
1×7 + 2×6 + 3×5 + 10×4 + 4×3 + 5×2 + 5×1 = 101
101 mod 11 = 2
```

Por tanto:

```text
K = 2
```

---

## Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con un entero:

```text
m
```

`m` representa la cantidad de regiones oscuras y claras detectadas por el lector:

```text
1 ≤ m ≤ 150
```

A continuación aparecen exactamente `m` enteros:

```text
d₁ d₂ d₃ ... dₘ
```

Cada valor `dᵢ` indica la cantidad de sensores que detectaron la región correspondiente:

```text
1 ≤ dᵢ ≤ 200
```

Las `m` medidas pueden estar distribuidas en varias líneas. El código siempre comienza y termina con una región oscura, por lo que no existe espacio en blanco inicial ni final dentro del código de barras.

La entrada termina con una línea que contiene:

```text
0
```

Ese cero no pertenece a ningún caso de prueba.

### Esquema de entrada

```text
m
d₁ d₂ ... dₘ
m
d₁ d₂ ... dₘ
0
```

---

## Formato de salida

Para cada caso se imprime una línea con el siguiente formato:

```text
Case número: resultado
```

Existen cuatro resultados posibles.

### Código válido

Si la estructura, el mensaje y ambos caracteres de verificación son correctos, se imprime el mensaje sin `C` ni `K`:

```text
Case 1: 123-45
```

### Código inválido

```text
Case 2: bad code
```

Se muestra `bad code` cuando no es posible decodificar el código debido a una condición como:

- Anchuras fuera del rango permitido.
- Cantidad incorrecta de regiones.
- Símbolo Start/Stop ausente o inválido.
- Separadores incorrectos.
- Algún grupo de cinco regiones no representa un carácter válido.
- Mensaje vacío.
- Cualquier otra estructura inválida.

### Carácter C incorrecto

```text
Case 3: bad C
```

Se muestra cuando el código puede decodificarse estructuralmente, pero el carácter `C` leído no coincide con el valor calculado.

### Carácter K incorrecto

```text
Case 4: bad K
```

Se muestra cuando el carácter `C` es correcto, pero el carácter `K` leído no coincide con el valor calculado.

La comprobación debe realizarse en este orden:

1. Validar la estructura del código.
2. Validar `C`.
3. Validar `K`.

---

## Ejemplo del resultado

Para los tres casos incluidos en el enunciado, la salida es:

```text
Case 1: 123-45
Case 2: bad code
Case 3: bad K
```

Esto significa que:

- El primer código contiene el mensaje válido `123-45`.
- El segundo no cumple la estructura de Code-11.
- El tercero tiene una estructura válida y un carácter `C` correcto, pero su carácter `K` es incorrecto.

---

## Resumen del objetivo

Para cada caso de prueba, el programa debe:

1. Interpretar las anchuras como regiones estrechas o anchas.
2. Considerar que el código puede estar invertido.
3. Separar las regiones en caracteres Code-11.
4. Validar los símbolos Start/Stop y los separadores.
5. Recuperar el mensaje y los caracteres `C` y `K`.
6. Comprobar los dos caracteres de verificación.
7. Imprimir el mensaje o el error correspondiente.
=======
<h1 align="center">
  <a href="#">
    Problem B
  </a>
</h1>

<p align="center">
  <strong>Barcodes</strong><br>
  @CIC-IPN Crisel Escalante, Octubre 2026
</p>

# Decodificador de códigos de barras Code-11

## Descripción del problema

Code-11 es un sistema de códigos de barras utilizado principalmente para identificar equipos de telecomunicaciones. Puede representar los dígitos del `0` al `9`, el guion `-` y un símbolo especial de inicio y fin llamado **Start/Stop**.

En este problema no se recibe una imagen del código de barras. Un lector ya ha escaneado el código y entrega una secuencia de números con las anchuras de las regiones oscuras y claras detectadas.

El objetivo es reconstruir el mensaje original, comprobar que la estructura del código sea válida y verificar dos caracteres de seguridad llamados `C` y `K`.

---

## Codificación de los caracteres

Cada carácter de Code-11 está formado por cinco regiones consecutivas que alternan entre:

```text
oscura, clara, oscura, clara, oscura
```

Cada región puede ser estrecha o ancha:

- `0`: región estrecha.
- `1`: región ancha.

La tabla de codificación es la siguiente:

| Carácter | Codificación |
|:--------:|:------------:|
| `0` | `00001` |
| `1` | `10001` |
| `2` | `01001` |
| `3` | `11000` |
| `4` | `00101` |
| `5` | `10100` |
| `6` | `01100` |
| `7` | `00011` |
| `8` | `10010` |
| `9` | `10000` |
| `-` | `00100` |
| Start/Stop | `00110` |

Por ejemplo, el carácter `1` se codifica como:

```text
10001
```

Esto representa, en orden:

1. Una región oscura ancha.
2. Una región clara estrecha.
3. Una región oscura estrecha.
4. Una región clara estrecha.
5. Una región oscura ancha.

Entre dos caracteres consecutivos siempre debe existir una región clara estrecha que funciona como separador.

---

## Anchuras de las regiones

Idealmente, una región ancha mide exactamente el doble que una región estrecha:

```text
ancha = 2 × estrecha
```

Sin embargo, la impresión del código puede ser imprecisa. Cada región puede medir hasta un `5%` más o un `5%` menos de su anchura esperada.

Si la anchura ideal de una región estrecha es `w`, entonces:

- Una región estrecha puede medir entre `0.95w` y `1.05w`.
- Una región ancha puede medir entre `1.90w` y `2.10w`.

Todas las medidas recibidas deben poder clasificarse de forma coherente como estrechas o anchas. Si esto no es posible, el código es inválido.

---

## Dirección del escaneo

El código de barras puede haber sido escaneado:

- De izquierda a derecha.
- De derecha a izquierda.

Por lo tanto, la secuencia de anchuras puede aparecer en el orden normal o completamente invertida. El programa debe reconocer ambas orientaciones.

---

## Estructura del código completo

Un código válido tiene la siguiente estructura:

```text
Start | mensaje | C | K | Stop
```

Donde:

- `Start` es el símbolo especial de inicio.
- `mensaje` contiene uno o más caracteres.
- `C` es el primer carácter de verificación.
- `K` es el segundo carácter de verificación.
- `Stop` es el símbolo especial de finalización.

No existen mensajes vacíos. Debe haber al menos un carácter entre `Start` y los caracteres de verificación.

Por ejemplo, si el mensaje es:

```text
123-45
```

sus caracteres de verificación son:

```text
C = 5
K = 2
```

La secuencia completa de caracteres codificados sería:

```text
Start 1 2 3 - 4 5 5 2 Stop
```

Al mostrar el resultado, solamente se imprime el mensaje original. Los caracteres `C`, `K`, `Start` y `Stop` no forman parte del mensaje mostrado.

---

## Peso de los caracteres

Para calcular los caracteres de verificación, cada símbolo tiene un peso numérico:

| Carácter | Peso |
|:--------:|:----:|
| `0` a `9` | `0` a `9` |
| `-` | `10` |

Si un cálculo produce el valor `10`, el carácter correspondiente es `-`.

---

## Carácter de verificación C

Supongamos que el mensaje contiene `n` caracteres:

```text
c₁, c₂, ..., cₙ
```

El peso del carácter `C` se calcula mediante:

```text
C = (Σ ((((n - i) mod 10) + 1) × peso(cᵢ))) mod 11
```

Los multiplicadores se aplican desde la derecha con la secuencia:

```text
1, 2, 3, ..., 10, 1, 2, ...
```

### Ejemplo

Para el mensaje:

```text
123-45
```

los pesos de los caracteres son:

```text
1, 2, 3, 10, 4, 5
```

Los multiplicadores correspondientes son:

```text
6, 5, 4, 3, 2, 1
```

Entonces:

```text
1×6 + 2×5 + 3×4 + 10×3 + 4×2 + 5×1 = 71
71 mod 11 = 5
```

Por tanto:

```text
C = 5
```

---

## Carácter de verificación K

Para calcular `K`, se utilizan los caracteres del mensaje y también el carácter `C` ya calculado.

Si `cₙ₊₁` representa el carácter `C`, entonces:

```text
K = (Σ ((((n - i + 1) mod 9) + 1) × peso(cᵢ))) mod 11
```

La suma se realiza para:

```text
i = 1 hasta n + 1
```

Los multiplicadores se aplican desde la derecha con la secuencia:

```text
1, 2, 3, ..., 9, 1, 2, ...
```

### Ejemplo

Para el mensaje `123-45`, sabemos que `C = 5`. Los caracteres usados para calcular `K` son:

```text
1 2 3 - 4 5 5
```

Sus multiplicadores son:

```text
7, 6, 5, 4, 3, 2, 1
```

Entonces:

```text
1×7 + 2×6 + 3×5 + 10×4 + 4×3 + 5×2 + 5×1 = 101
101 mod 11 = 2
```

Por tanto:

```text
K = 2
```

---

## Formato de entrada

La entrada contiene varios casos de prueba.

Cada caso comienza con un entero:

```text
m
```

`m` representa la cantidad de regiones oscuras y claras detectadas por el lector:

```text
1 ≤ m ≤ 150
```

A continuación aparecen exactamente `m` enteros:

```text
d₁ d₂ d₃ ... dₘ
```

Cada valor `dᵢ` indica la cantidad de sensores que detectaron la región correspondiente:

```text
1 ≤ dᵢ ≤ 200
```

Las `m` medidas pueden estar distribuidas en varias líneas. El código siempre comienza y termina con una región oscura, por lo que no existe espacio en blanco inicial ni final dentro del código de barras.

La entrada termina con una línea que contiene:

```text
0
```

Ese cero no pertenece a ningún caso de prueba.

### Esquema de entrada

```text
m
d₁ d₂ ... dₘ
m
d₁ d₂ ... dₘ
0
```

---

## Formato de salida

Para cada caso se imprime una línea con el siguiente formato:

```text
Case número: resultado
```

Existen cuatro resultados posibles.

### Código válido

Si la estructura, el mensaje y ambos caracteres de verificación son correctos, se imprime el mensaje sin `C` ni `K`:

```text
Case 1: 123-45
```

### Código inválido

```text
Case 2: bad code
```

Se muestra `bad code` cuando no es posible decodificar el código debido a una condición como:

- Anchuras fuera del rango permitido.
- Cantidad incorrecta de regiones.
- Símbolo Start/Stop ausente o inválido.
- Separadores incorrectos.
- Algún grupo de cinco regiones no representa un carácter válido.
- Mensaje vacío.
- Cualquier otra estructura inválida.

### Carácter C incorrecto

```text
Case 3: bad C
```

Se muestra cuando el código puede decodificarse estructuralmente, pero el carácter `C` leído no coincide con el valor calculado.

### Carácter K incorrecto

```text
Case 4: bad K
```

Se muestra cuando el carácter `C` es correcto, pero el carácter `K` leído no coincide con el valor calculado.

La comprobación debe realizarse en este orden:

1. Validar la estructura del código.
2. Validar `C`.
3. Validar `K`.

---

## Ejemplo del resultado

Para los tres casos incluidos en el enunciado, la salida es:

```text
Case 1: 123-45
Case 2: bad code
Case 3: bad K
```

Esto significa que:

- El primer código contiene el mensaje válido `123-45`.
- El segundo no cumple la estructura de Code-11.
- El tercero tiene una estructura válida y un carácter `C` correcto, pero su carácter `K` es incorrecto.

---

## Resumen del objetivo

Para cada caso de prueba, el programa debe:

1. Interpretar las anchuras como regiones estrechas o anchas.
2. Considerar que el código puede estar invertido.
3. Separar las regiones en caracteres Code-11.
4. Validar los símbolos Start/Stop y los separadores.
5. Recuperar el mensaje y los caracteres `C` y `K`.
6. Comprobar los dos caracteres de verificación.
7. Imprimir el mensaje o el error correspondiente.
