"""
Stuck Squares - solución con compresión de coordenadas y DP.

Ejemplo de entrada:

8 8 3
1 6 3 6
2 4 2 4
4 2 7 2
0 0 0

Salida correspondiente:

Case 1: 8
"""

import sys


def count_stuck_squares(rows, columns, walls):
    """Cuenta los cuadrados libres que no pueden alcanzar la salida."""

    # Guardamos solamente las coordenadas donde comienza o termina
    # una pared. También incluimos los límites de la habitación.
    x_coordinates = {0, columns}
    y_coordinates = {0, rows}

    for x1, y1, x2, y2 in walls:
        x_coordinates.add(x1)
        x_coordinates.add(x2 + 1)
        y_coordinates.add(y1)
        y_coordinates.add(y1 + 1)

    # Las coordenadas consecutivas forman los rectángulos comprimidos.
    xs = sorted(x_coordinates)
    ys = sorted(y_coordinates)

    compressed_columns = len(xs) - 1
    compressed_rows = len(ys) - 1

    # Estos diccionarios permiten convertir una coordenada original
    # en su índice dentro de la cuadrícula comprimida.
    x_index = {coordinate: index for index, coordinate in enumerate(xs)}
    y_index = {coordinate: index for index, coordinate in enumerate(ys)}

    # blocked[y][x] vale 1 si el rectángulo comprimido está ocupado.
    # bytearray usa aproximadamente un byte por posición.
    blocked = [bytearray(compressed_columns) for _ in range(compressed_rows)]

    for x1, y1, x2, y2 in walls:
        row = y_index[y1]
        beginning = x_index[x1]
        ending = x_index[x2 + 1]

        # La pared ocupa los intervalos [beginning, ending).
        blocked[row][beginning:ending] = b"\x01" * (ending - beginning)

    # Anchura real de cada columna comprimida. Se calcula una sola vez
    # porque se utilizará al sumar las áreas atascadas.
    column_widths = [xs[index + 1] - xs[index] for index in range(compressed_columns)]

    # north_row indica qué regiones de la fila inmediatamente al norte
    # pueden llegar a la salida. Al comenzar no existe una fila superior.
    north_row = bytearray(compressed_columns)

    last_row = compressed_rows - 1
    last_column = compressed_columns - 1
    stuck_squares = 0

    # Recorremos desde el norte hacia el sur.
    for row in range(last_row, -1, -1):
        current_row = bytearray(compressed_columns)
        row_height = ys[row + 1] - ys[row]
        blocked_row = blocked[row]

        # Mientras recorremos de este a oeste, esta variable representa
        # si la región inmediatamente al este alcanza la salida.
        east_reachable = False

        for column in range(last_column, -1, -1):
            if blocked_row[column]:
                # Una pared tampoco puede servir de camino para la región
                # que se encuentre inmediatamente al oeste.
                east_reachable = False
                continue

            contains_exit = row == last_row and column == last_column

            # Desde una región libre solo podemos ir al norte o al este.
            reachable = contains_exit or bool(north_row[column]) or east_reachable

            if reachable:
                current_row[column] = 1
            else:
                # Toda la región comprimida está atascada. Sumamos la
                # cantidad de cuadrados originales que representa.
                stuck_squares += column_widths[column] * row_height

            # Para la siguiente región hacia el oeste, la región actual
            # será su vecina del este.
            east_reachable = reachable

        # La fila actual se convierte en la fila norte de la próxima
        # iteración. No necesitamos conservar las filas anteriores.
        north_row = current_row

    return stuck_squares


def solve():
    input_stream = sys.stdin.buffer
    answers = []
    case_number = 1

    while True:
        line = input_stream.readline()

        # También terminamos si el archivo finaliza sin 0 0 0.
        if not line:
            break

        # Ignoramos posibles líneas vacías.
        if not line.strip():
            continue

        rows, columns, wall_count = map(int, line.split())

        if rows == 0 and columns == 0 and wall_count == 0:
            break

        walls = []

        for _ in range(wall_count):
            x1, y1, x2, y2 = map(int, input_stream.readline().split())
            walls.append((x1, y1, x2, y2))

        result = count_stuck_squares(rows, columns, walls)
        answers.append(f"Case {case_number}: {result}")
        case_number += 1

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
