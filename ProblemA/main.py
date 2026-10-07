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
        self.tokens = line.split()
        self.pos = 0

    def current(self):
        if self.pos == len(self.tokens):
            return None
        return self.tokens[self.pos]

    def next_token(self):
        if self.pos + 1 >= len(self.tokens):
            return None
        return self.tokens[self.pos + 1]

    def parse(self):
        return self.expression()

    def expression(self):
        if self.current() == "iota":
            self.pos += 1
            return ("iota", self.expression())

        if self.current() in {"+", "-", "*"} and self.next_token() == "/":
            operator = self.current()
            self.pos += 2
            return ("reduce", operator, self.expression())

        left = self.value()

        if self.current() in OPERATORS:
            operator = self.current()
            self.pos += 1
            right = self.expression()

            return (operator, left, right)

        return left

    def value(self):
        if self.current() == "(":
            self.pos += 1
            result = self.expression()

            # Saltamos el paréntesis ")"
            self.pos += 1
            return result

        if self.current().isdigit():
            numbers = []

            while self.current() is not None and self.current().isdigit():
                numbers.append(int(self.current()))
                self.pos += 1

            return ("constant", numbers)

        name = self.current()
        self.pos += 1

        return ("variable", name)


def calculate(operator, a, b):
    if operator == "+":
        return a + b

    if operator == "-":
        return a - b

    return a * b


def arithmetic(operator, left, right):
    left_shape, left_data = left
    right_shape, right_data = right

    if left_shape == right_shape:
        shape = left_shape

    elif len(left_data) == 1:
        shape = right_shape
        left_data = left_data * len(right_data)

    else:
        shape = left_shape
        right_data = right_data * len(left_data)

    data = [calculate(operator, a, b) for a, b in zip(left_data, right_data)]

    return shape, data


def reshape(left, right):
    shape = tuple(left[1])
    source = right[1]
    size = 1

    for dimension in shape:
        size *= dimension

    data = [source[i % len(source)] for i in range(size)]

    return shape, data


def reduce_array(operator, array):
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
