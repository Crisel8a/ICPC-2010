"""
Contour Mapping - suma de contornos sobre una malla triangular.

Ejemplo de entrada:

3 2 5 5
1 1
1 9 1
1 1

4 4 5 3
5 7 7 5
5 9 9 9 5
9 9 9 9
7 9 9 9 7

0

Salida correspondiente:

Case 1: 15
Case 2: 54
"""

import math
import sys


def arithmetic_level_sum(first_index, last_index, increment):
    """Suma los niveles k*h desde first_index hasta last_index."""

    count = last_index - first_index + 1

    # La suma first + ... + last es:
    # (first + last) * count / 2.
    index_sum = (first_index + last_index) * count // 2

    return count, index_sum * increment


def build_mesh(scan_lines, side_length):
    """Construye puntos, triángulos y adyacencias de aristas."""

    vertical_distance = side_length * math.sqrt(3.0) / 2.0

    points = []
    row_point_ids = []

    for row, elevations in enumerate(scan_lines):
        # Las filas con p puntos están desplazadas medio lado.
        horizontal_offset = side_length / 2.0 if row % 2 == 0 else 0.0
        point_ids = []

        for column, elevation in enumerate(elevations):
            x = horizontal_offset + column * side_length
            y = row * vertical_distance

            points.append((x, y, elevation))
            point_ids.append(len(points) - 1)

        row_point_ids.append(point_ids)

    triangles = []
    small_row_size = len(scan_lines[0])

    # Entre dos filas consecutivas hay una fila pequeña de p puntos
    # y una fila grande de p + 1 puntos.
    for row in range(len(row_point_ids) - 1):
        first_row = row_point_ids[row]
        second_row = row_point_ids[row + 1]

        if len(first_row) < len(second_row):
            small_row = first_row
            large_row = second_row
        else:
            small_row = second_row
            large_row = first_row

        # Triángulos cuya base usa dos puntos de la fila grande.
        for column in range(small_row_size):
            triangles.append(
                (
                    small_row[column],
                    large_row[column],
                    large_row[column + 1],
                )
            )

        # Triángulos cuya base usa dos puntos de la fila pequeña.
        for column in range(small_row_size - 1):
            triangles.append(
                (
                    small_row[column],
                    small_row[column + 1],
                    large_row[column + 1],
                )
            )

    # Para cada arista guardamos:
    # [cantidad de triángulos adyacentes, cantidad de esos triángulos
    #  que son completamente planos].
    edge_information = {}

    for triangle in triangles:
        first, second, third = triangle

        first_height = points[first][2]
        second_height = points[second][2]
        third_height = points[third][2]

        is_flat = first_height == second_height == third_height

        for endpoint_a, endpoint_b in (
            (first, second),
            (second, third),
            (third, first),
        ):
            edge = (
                min(endpoint_a, endpoint_b),
                max(endpoint_a, endpoint_b),
            )

            if edge not in edge_information:
                edge_information[edge] = [0, 0]

            edge_information[edge][0] += 1

            if is_flat:
                edge_information[edge][1] += 1

    return points, triangles, edge_information


def triangle_contour_length(points, triangle, increment, side_length):
    """Suma en O(1) todos los contornos interiores de un triángulo."""

    vertices = sorted(
        (points[point_id] for point_id in triangle),
        key=lambda vertex: vertex[2],
    )

    x0, y0, z0 = vertices[0]
    x1, y1, z1 = vertices[1]
    x2, y2, z2 = vertices[2]

    # Un triángulo completamente plano no tiene segmentos interiores.
    # Sus fronteras se procesarán mediante las aristas.
    if z0 == z2:
        return 0.0

    # P es la longitud máxima del corte, situada en la elevación z1.
    if z0 == z1 or z1 == z2:
        peak_length = float(side_length)
    else:
        interpolation = (z1 - z0) / (z2 - z0)

        interpolated_x = x0 + interpolation * (x2 - x0)
        interpolated_y = y0 + interpolation * (y2 - y0)

        peak_length = math.hypot(
            x1 - interpolated_x,
            y1 - interpolated_y,
        )

    total = 0.0

    # ---------------------------------------------------------------
    # Tramo inferior:
    # length(L) = P * (L - z0) / (z1 - z0)
    # ---------------------------------------------------------------
    if z1 > z0:
        first_index = z0 // increment + 1

        if z1 < z2:
            # Si z1 es una elevación única, su nivel se incluye aquí.
            last_index = z1 // increment
        else:
            # Si z1 == z2, el nivel superior coincide con una arista y
            # será procesado aparte.
            last_index = (z1 - 1) // increment

        if first_index <= last_index:
            count, level_sum = arithmetic_level_sum(
                first_index,
                last_index,
                increment,
            )

            total += peak_length * (level_sum - count * z0) / (z1 - z0)

    # ---------------------------------------------------------------
    # Tramo superior:
    # length(L) = P * (z2 - L) / (z2 - z1)
    # ---------------------------------------------------------------
    if z2 > z1:
        first_index = z1 // increment + 1

        # El máximo z2 solo produce un punto, o una arista si está
        # repetido. En ambos casos no pertenece al segmento interior.
        last_index = (z2 - 1) // increment

        if first_index <= last_index:
            count, level_sum = arithmetic_level_sum(
                first_index,
                last_index,
                increment,
            )

            total += peak_length * (count * z2 - level_sum) / (z2 - z1)

    return total


def total_contour_length(scan_lines, side_length, increment):
    """Calcula la longitud total de todas las líneas de contorno."""

    points, triangles, edge_information = build_mesh(
        scan_lines,
        side_length,
    )

    total = 0.0

    # Sumamos todos los segmentos que atraviesan interiores de triángulos.
    for triangle in triangles:
        total += triangle_contour_length(
            points,
            triangle,
            increment,
            side_length,
        )

    # Procesamos las líneas de contorno que coinciden exactamente con
    # aristas de la triangulación.
    for edge, information in edge_information.items():
        endpoint_a, endpoint_b = edge
        adjacent_count, flat_count = information

        height_a = points[endpoint_a][2]
        height_b = points[endpoint_b][2]

        if height_a != height_b:
            continue

        if height_a % increment != 0:
            continue

        # Si ambos triángulos adyacentes son planos, la arista está en el
        # interior de una región nivelada y no debe dibujarse.
        if adjacent_count == 2 and flat_count == 2:
            continue

        total += side_length

    return total


def read_numbers():
    """Lee enteros progresivamente e ignora líneas vacías."""

    for line in sys.stdin.buffer:
        for token in line.split():
            yield int(token)


def solve():
    numbers = iter(read_numbers())
    answers = []
    case_number = 1

    while True:
        try:
            scan_line_count = next(numbers)
        except StopIteration:
            break

        if scan_line_count == 0:
            break

        points_on_odd_lines = next(numbers)
        side_length = next(numbers)
        increment = next(numbers)

        scan_lines = []

        for row in range(scan_line_count):
            point_count = (
                points_on_odd_lines if row % 2 == 0 else points_on_odd_lines + 1
            )

            scan_lines.append([next(numbers) for _ in range(point_count)])

        total = total_contour_length(
            scan_lines,
            side_length,
            increment,
        )

        # La longitud es positiva. floor(total + 0.5) implementa el
        # redondeo tradicional al entero más cercano.
        rounded_total = math.floor(total + 0.5 + 1e-9)

        answers.append(f"Case {case_number}: {rounded_total}")
        case_number += 1

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
