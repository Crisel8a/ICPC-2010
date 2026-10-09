"""
Ejemplo de uso
--------------

El siguiente código representa el mensaje "0". Sus caracteres C y K
también son "0", por lo que la secuencia completa es:

    Start | 0 | 0 | 0 | Stop

Entrada:

29
10 10 20 20 10 10
10 10 10 10 20 10
10 10 10 10 20 10
10 10 10 10 20 10
10 10 20 20 10
0

Salida:

Case 1: 0
"""

import sys

# Cada patrón tiene cinco regiones.
# 0 significa estrecha y 1 significa ancha.
PATTERN_TO_CHAR = {
    "00001": "0",
    "10001": "1",
    "01001": "2",
    "11000": "3",
    "00101": "4",
    "10100": "5",
    "01100": "6",
    "00011": "7",
    "10010": "8",
    "10000": "9",
    "00100": "-",
    "00110": "START_STOP",
}


def classify_widths(widths):
    """Convierte cada anchura en 0 (estrecha) o 1 (ancha)."""

    narrowest = min(widths)

    # En un código válido hay una separación grande entre ambos grupos:
    # una estrecha mide cerca de w y una ancha cerca de 2w.
    # El valor 1.5w sirve como frontera entre los dos grupos.
    bits = [0 if 2 * width < 3 * narrowest else 1 for width in widths]

    # Todas las regiones deben ser compatibles con una misma anchura
    # ideal w. Calculamos el intervalo posible para ese valor.
    minimum_w = 0.0
    maximum_w = float("inf")

    for width, bit in zip(widths, bits):
        if bit == 0:
            # 0.95w <= width <= 1.05w
            lower = width / 1.05
            upper = width / 0.95
        else:
            # 1.90w <= width <= 2.10w
            lower = width / 2.10
            upper = width / 1.90

        minimum_w = max(minimum_w, lower)
        maximum_w = min(maximum_w, upper)

    # Si los intervalos no se cruzan, no existe una anchura ideal común.
    if minimum_w > maximum_w + 1e-9:
        return None

    return bits


def decode_in_one_direction(bits):
    """Intenta separar y decodificar los símbolos en una orientación."""

    # Cada símbolo usa cinco regiones. Entre dos símbolos hay un
    # separador, así que para t símbolos existen 6t - 1 regiones.
    if (len(bits) + 1) % 6 != 0:
        return None

    symbol_count = (len(bits) + 1) // 6

    # Se necesitan Start, al menos un carácter, C, K y Stop.
    if symbol_count < 5:
        return None

    characters = []
    position = 0

    for symbol_index in range(symbol_count):
        pattern = "".join(str(bit) for bit in bits[position : position + 5])

        if pattern not in PATTERN_TO_CHAR:
            return None

        characters.append(PATTERN_TO_CHAR[pattern])
        position += 5

        # Entre dos símbolos debe existir una región clara estrecha.
        if symbol_index < symbol_count - 1:
            if bits[position] != 0:
                return None
            position += 1

    # El primer y último símbolo deben ser Start/Stop.
    if characters[0] != "START_STOP":
        return None

    if characters[-1] != "START_STOP":
        return None

    # Start/Stop no puede aparecer dentro del mensaje.
    if "START_STOP" in characters[1:-1]:
        return None

    # Eliminamos Start y Stop. Quedan mensaje + C + K.
    return characters[1:-1]


def character_weight(character):
    """Devuelve el peso numérico de un carácter Code-11."""

    if character == "-":
        return 10

    return int(character)


def calculate_check_character(characters, cycle):
    """Calcula C con ciclo 10 o K con ciclo 9."""

    count = len(characters)
    total = 0

    for index, character in enumerate(characters, start=1):
        multiplier = ((count - index) % cycle) + 1
        total += multiplier * character_weight(character)

    result = total % 11

    if result == 10:
        return "-"

    return str(result)


def decode_barcode(widths):
    """Decodifica un caso completo y devuelve el mensaje o su error."""

    bits = classify_widths(widths)

    if bits is None:
        return "bad code"

    # Primero intentamos leer tal como llegó el código.
    decoded = decode_in_one_direction(bits)

    # Si falla, pudo haber sido escaneado de derecha a izquierda.
    if decoded is None:
        decoded = decode_in_one_direction(bits[::-1])

    if decoded is None:
        return "bad code"

    # decoded contiene: mensaje + C + K.
    # Por tanto, debe contener al menos tres caracteres.
    if len(decoded) < 3:
        return "bad code"

    message = decoded[:-2]
    given_c = decoded[-2]
    given_k = decoded[-1]

    expected_c = calculate_check_character(message, 10)

    if given_c != expected_c:
        return "bad C"

    # Para calcular K se usa el mensaje y también C.
    expected_k = calculate_check_character(message + [given_c], 9)

    if given_k != expected_k:
        return "bad K"

    return "".join(message)


def solve():
    # Leemos los números poco a poco. De esta manera el programa
    # termina inmediatamente cuando escribimos 0 y presionamos Enter.
    def read_numbers():
        for line in sys.stdin:
            for token in line.split():
                yield int(token)

    numbers = iter(read_numbers())
    case_number = 1
    answers = []

    while True:
        try:
            region_count = next(numbers)
        except StopIteration:
            break

        if region_count == 0:
            break

        widths = [next(numbers) for _ in range(region_count)]

        result = decode_barcode(widths)
        answers.append(f"Case {case_number}: {result}")
        case_number += 1

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
