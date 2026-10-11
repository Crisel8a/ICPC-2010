"""
Shortest Path in Two Passes - programación dinámica bitónica.

Ejemplo de entrada:

5 1 3
1 3
3 4
4 1
7 5
8 3
5 3 2
0 10
3 14
4 7
7 10
8 12
0 0 0

Salida correspondiente:

Case 1: 18.18
0 1 4 3 2 0
Case 2: 24.30
0 1 3 4 2 0
"""

import math
import sys


def build_distances(points):
    """Precalcula la distancia euclidiana entre cada par de islas."""

    island_count = len(points)
    distances = [[0.0] * island_count for _ in range(island_count)]

    for first in range(island_count):
        x1, y1 = points[first]

        for second in range(first + 1, island_count):
            x2, y2 = points[second]

            distance = math.hypot(
                x2 - x1,
                y2 - y1,
            )

            distances[first][second] = distance
            distances[second][first] = distance

    return distances


def shortest_tour(points, special_first, special_second):
    """
    Devuelve la longitud mínima y el orden de visita.

    special_first se coloca en la pasada hacia el este.
    special_second se coloca en la pasada de regreso.
    """

    island_count = len(points)
    last_island = island_count - 1
    distances = build_distances(points)

    # Un estado (i, j) representa dos caminos parciales:
    #
    #   Camino A termina en i.
    #   Camino B termina en j.
    #
    # Todas las islas hasta max(i, j) ya fueron asignadas.
    current_states = {(0, 0): 0.0}

    # parents[state] = (previous_state, chosen_path)
    # chosen_path vale "A" o "B".
    parents = {}

    # La isla final pertenece a ambos caminos, así que únicamente
    # asignamos las islas intermedias 1 .. n - 2.
    for next_island in range(1, last_island):
        next_states = {}

        for state, current_cost in current_states.items():
            end_a, end_b = state

            # ---------------------------------------------------------
            # Opción 1: añadir la isla al camino A.
            # No está permitido si es la isla especial del camino B.
            # ---------------------------------------------------------
            if next_island != special_second:
                new_state = (next_island, end_b)
                new_cost = current_cost + distances[end_a][next_island]

                previous_cost = next_states.get(new_state)

                if previous_cost is None or new_cost < previous_cost - 1e-12:
                    next_states[new_state] = new_cost
                    parents[new_state] = (state, "A")

            # ---------------------------------------------------------
            # Opción 2: añadir la isla al camino B.
            # No está permitido si es la isla especial del camino A.
            # ---------------------------------------------------------
            if next_island != special_first:
                new_state = (end_a, next_island)
                new_cost = current_cost + distances[end_b][next_island]

                previous_cost = next_states.get(new_state)

                if previous_cost is None or new_cost < previous_cost - 1e-12:
                    next_states[new_state] = new_cost
                    parents[new_state] = (state, "B")

        current_states = next_states

    # Ambos caminos deben terminar en la isla más oriental.
    best_cost = float("inf")
    best_state = None

    for state, current_cost in current_states.items():
        end_a, end_b = state

        complete_cost = (
            current_cost + distances[end_a][last_island] + distances[end_b][last_island]
        )

        if complete_cost < best_cost - 1e-12:
            best_cost = complete_cost
            best_state = state

    # ---------------------------------------------------------------
    # Reconstrucción de la asignación de islas.
    # ---------------------------------------------------------------
    path_a_reversed = []
    path_b_reversed = []

    state = best_state

    while state != (0, 0):
        previous_state, chosen_path = parents[state]

        if chosen_path == "A":
            # La primera coordenada fue la isla añadida.
            path_a_reversed.append(state[0])
        else:
            # La segunda coordenada fue la isla añadida.
            path_b_reversed.append(state[1])

        state = previous_state

    path_a = [0]
    path_a.extend(reversed(path_a_reversed))
    path_a.append(last_island)

    path_b = [0]
    path_b.extend(reversed(path_b_reversed))
    path_b.append(last_island)

    # La primera pasada recorre A de oeste a este. Después recorremos
    # B al revés, sin repetir la isla oriental.
    tour = path_a + list(reversed(path_b[:-1]))

    return best_cost, tour


def read_numbers():
    """Lee enteros progresivamente y permite terminar con 0 0 0."""

    for line in sys.stdin.buffer:
        for token in line.split():
            yield int(token)


def solve():
    numbers = iter(read_numbers())
    output = []
    case_number = 1

    while True:
        try:
            island_count = next(numbers)
            special_first = next(numbers)
            special_second = next(numbers)
        except StopIteration:
            break

        if island_count == 0 and special_first == 0 and special_second == 0:
            break

        points = [(next(numbers), next(numbers)) for _ in range(island_count)]

        length, tour = shortest_tour(
            points,
            special_first,
            special_second,
        )

        # Una tolerancia mínima evita errores binarios justo antes
        # de una frontera de redondeo.
        output.append(f"Case {case_number}: {length + 1e-9:.2f}")
        output.append(" ".join(map(str, tour)))

        case_number += 1

    print("\n".join(output))


if __name__ == "__main__":
    solve()
