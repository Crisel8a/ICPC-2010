"""
Ejemplo de entrada:

var = 1 2 3
var + 4
iota 5
2 2 rho 1 2 3 4
#

Salida:

Case 1: var = 1 2 3
1 2 3
Case 2: var + 4
5 6 7
Case 3: iota 5
1 2 3 4 5
Case 4: 2 2 rho 1 2 3 4
1 2
3 4
"""

import sys

OPERATORS = {"=", "+", "-", "*", "rho", "drop"}


class Parser:
    def __init__(self, line):
        self.tokens = line.split()  # dividimos la línea en tokens
        self.pos = 0

    def current(self):
        if self.pos == len(
            self.tokens
        ):  # si llegamos al final de la lista de tokens, devolvemos None
            return None
        return self.tokens[self.pos]  # si no, devolvemos el token actual

    def next_token(self):
        if (
            self.pos + 1 >= len(self.tokens)
        ):  # si el siguiente token está fuera de los límites de la lista, devolvemos None
            return None
        return self.tokens[self.pos + 1]  # si no, devolvemos el siguiente token

    def parse(self):
        return (
            self.expression()
        )  # iniciamos el análisis sintáctico con la función expression

    def expression(self):
        if (
            self.current() == "iota"
        ):  # si el token actual es "iota", avanzamos al siguiente token y analizamos la expresión que sigue
            self.pos += 1  # avanzamos al siguiente token
            return (
                "iota",
                self.expression(),
            )  # devolvemos una tupla con el operador "iota" y la expresión que sigue

        if (
            self.current() in {"+", "-", "*"} and self.next_token() == "/"
        ):  # si el token actual es un operador y el siguiente token es "/", avanzamos dos tokens y analizamos la expresión que sigue
            operator = self.current()  # guardamos el operador actual
            self.pos += 2
            return (
                "reduce",
                operator,
                self.expression(),
            )  # devolvemos una tupla con el operador "reduce", el operador actual y la expresión que sigue

        left = self.value()  # analizamos el valor izquierdo de la expresión

        if (
            self.current() in OPERATORS
        ):  # si el token actual es un operador, guardamos el operador y analizamos la expresión que sigue
            operator = self.current()
            self.pos += 1
            right = self.expression()  # analizamos el valor derecho de la expresión

            return (
                operator,
                left,
                right,
            )  # devolvemos una tupla con el operador, el valor izquierdo y el valor derecho

        return left  # si no hay operador, devolvemos el valor izquierdo

    def value(
        self,
    ):  # analizamos un valor, que puede ser un número, una variable o una expresión entre paréntesis
        if (
            self.current() == "("
        ):  # si el token actual es un paréntesis de apertura, analizamos la expresión dentro de los paréntesis
            self.pos += 1
            result = (
                self.expression()
            )  # analizamos la expresión dentro de los paréntesis

            # Saltamos el paréntesis ")"
            self.pos += 1
            return result  # devolvemos el resultado de la expresión dentro de los paréntesis

        if self.current().isdigit():  # si el token actual es un número, lo convertimos a entero y lo devolvemos como una constante
            numbers = []

            while (
                self.current() is not None and self.current().isdigit()
            ):  # mientras haya tokens y el token actual sea un número, lo convertimos a entero y lo agregamos a la lista de números
                numbers.append(
                    int(self.current())
                )  # convertimos el token actual a entero y lo agregamos a la lista de números
                self.pos += 1

            return (
                "constant",
                numbers,
            )  # devolvemos una tupla con el tipo "constant" y la lista de números

        name = self.current()
        self.pos += 1

        return (
            "variable",
            name,
        )  # si el token actual no es un número ni un paréntesis, lo tratamos como una variable y lo devolvemos como tal


def calculate(
    operator, a, b
):  # realizamos la operación aritmética correspondiente según el operador
    if operator == "+":
        return a + b

    if operator == "-":
        return a - b

    return a * b


def arithmetic(operator, left, right):
    left_shape, left_data = (
        left  # obtenemos la forma y los datos del lado izquierdo de la operación
    )
    right_shape, right_data = (
        right  # obtenemos la forma y los datos del lado derecho de la operación
    )

    if (
        left_shape == right_shape
    ):  # si las formas de los dos lados son iguales, realizamos la operación elemento por elemento
        shape = left_shape

    elif (
        len(left_data) == 1
    ):  # si el lado izquierdo tiene un solo elemento, repetimos ese elemento para que coincida con la longitud del lado derecho
        shape = right_shape
        left_data = (
            left_data * len(right_data)
        )  # repetimos el elemento del lado izquierdo para que coincida con la longitud del lado derecho

    else:
        shape = left_shape  # si el lado derecho tiene un solo elemento, repetimos ese elemento para que coincida con la longitud del lado izquierdo
        right_data = right_data * len(left_data)

    data = [calculate(operator, a, b) for a, b in zip(left_data, right_data)]

    return shape, data


def reshape(
    left, right
):  # obtenemos la forma y los datos del lado izquierdo y derecho de la operación de reshape
    shape = tuple(
        left[1]
    )  # convertimos la lista de dimensiones del lado izquierdo en una tupla para representar la nueva forma del arreglo
    source = right[1]  # obtenemos los datos del lado derecho de la operación de reshape
    size = 1

    for dimension in shape:
        size *= dimension

    data = [source[i % len(source)] for i in range(size)]

    return shape, data


def reduce_array(operator, array):
    # realizamos la reducción de un arreglo según el operador especificado
    shape, data = array
    row_size = shape[-1]
    result = []

    for start in range(0, len(data), row_size):
        row = data[start : start + row_size]

        # La reducción empieza desde la derecha
        value = row[-1]

        for number in reversed(row[:-1]):
            value = calculate(operator, number, value)

        result.append(value)

    if len(shape) == 1:
        new_shape = (1,)
    else:
        new_shape = shape[:-1]

    return new_shape, result


def evaluate(node, variables):
    kind = node[0]

    if kind == "constant":
        numbers = node[1]
        return (len(numbers),), numbers

    if kind == "variable":
        return variables[node[1]]

    if kind == "iota":
        operand = evaluate(node[1], variables)
        number = operand[1][0]

        return ((number,), list(range(1, number + 1)))

    if kind == "reduce":
        operand = evaluate(node[2], variables)

        return reduce_array(node[1], operand)

    operator, left_node, right_node = node

    # APL evalúa primero el lado derecho
    right = evaluate(right_node, variables)

    if operator == "=":
        variable_name = left_node[1]
        variables[variable_name] = right

        return right

    left = evaluate(left_node, variables)

    if operator in {"+", "-", "*"}:
        return arithmetic(operator, left, right)

    if operator == "rho":
        return reshape(left, right)

    # La única operación restante es drop
    amount = left[1][0]
    data = right[1][amount:]

    return (len(data),), data


def format_array(array):
    shape, data = array

    # Vector
    if len(shape) == 1:
        return [" ".join(map(str, data))]

    rows = shape[-2]
    columns = shape[-1]

    if len(shape) == 2:
        planes = 1
    else:
        planes = shape[0]

    lines = []

    for plane in range(planes):
        # Separar matrices de un arreglo 3D
        if plane > 0:
            lines.append("")

        for row in range(rows):
            start = plane * rows * columns + row * columns

            values = data[start : start + columns]

            lines.append(" ".join(map(str, values)))

    return lines


def solve():
    variables = {}
    output = []
    case_number = 1

    for raw_line in sys.stdin:
        line = raw_line.rstrip("\n")

        if line == "#":
            break

        tree = Parser(line).parse()
        result = evaluate(tree, variables)

        output.append(f"Case {case_number}: {line}")

        output.extend(format_array(result))
        case_number += 1

    print("\n".join(output))


if __name__ == "__main__":
    solve()
