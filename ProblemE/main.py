"""
Irrigation Channel - programación dinámica de perfil.

Ejemplo de entrada:

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

Salida correspondiente:

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
"""

import sys
from functools import cache


def encode_entry(label, degree):
    """Guarda etiqueta y grado en un solo entero."""

    return label * 3 + degree


def entry_label(entry):
    return entry // 3


def entry_degree(entry):
    return entry % 3


@cache
def normalize_frontier(frontier):
    """Renombra las componentes como 1, 2, 3... de izquierda a derecha."""

    new_labels = {}
    next_label = 1
    normalized = []

    for entry in frontier:
        if entry == 0:
            normalized.append(0)
            continue

        label = entry_label(entry)
        degree = entry_degree(entry)

        if label not in new_labels:
            new_labels[label] = next_label
            next_label += 1

        normalized.append(encode_entry(new_labels[label], degree))

    return tuple(normalized)


def save_best(states, key, length, channel_mask):
    """Conserva solamente el camino más largo para un mismo estado."""

    previous = states.get(key)

    if previous is None or length > previous[0]:
        states[key] = (length, channel_mask)


def longest_channel(field):
    """Devuelve una máscara con las celdas del canal óptimo."""

    rows = len(field)
    columns = len(field[0])

    empty_frontier = (0,) * columns

    # La clave contiene:
    #   1. La frontera.
    #   2. Si la celda superior izquierda estaba seleccionada.
    #
    # El valor contiene:
    #   1. La longitud conseguida.
    #   2. La máscara de celdas seleccionadas.
    states = {(empty_frontier, False, False): (0, 0)}

    for row in range(rows):
        for column in range(columns):
            next_states = {}

            is_start = row == 0 and column == 0
            is_end = row == rows - 1 and column == columns - 1
            is_required = is_start or is_end
            is_rock = field[row][column] == "#"

            for state, value in states.items():
                frontier, upper_left_selected, must_select_current = state
                length, channel_mask = value

                # Antes de reemplazar esta posición, contiene la celda
                # situada arriba de la celda actual.
                upper_entry = frontier[column]

                # Después de esta transición, upper_entry será la celda
                # superior izquierda de la siguiente columna.
                next_upper_left = bool(upper_entry)

                # Al comenzar una nueva fila ya no necesitamos ese dato.
                if column == columns - 1:
                    next_upper_left = False

                # -----------------------------------------------------
                # Opción 1: dejar la celda actual vacía.
                # -----------------------------------------------------
                if not is_required and not must_select_current:
                    new_frontier = list(frontier)
                    new_frontier[column] = 0
                    valid = True

                    if upper_entry:
                        upper_degree = entry_degree(upper_entry)

                        # La única esquina que puede salir de la frontera
                        # durante el procesamiento es la entrada.
                        expected_degree = 1 if row - 1 == 0 and column == 0 else 2

                        if upper_degree != expected_degree:
                            valid = False
                        else:
                            upper_label = entry_label(upper_entry)

                            # Una componente no puede desaparecer antes de
                            # haber alcanzado la salida.
                            component_survives = any(
                                entry and entry_label(entry) == upper_label
                                for entry in new_frontier
                            )

                            if not component_survives:
                                valid = False

                    if valid:
                        normalized = normalize_frontier(tuple(new_frontier))
                        key = (normalized, next_upper_left, False)
                        save_best(
                            next_states,
                            key,
                            length,
                            channel_mask,
                        )

                # -----------------------------------------------------
                # Opción 2: colocar canal en la celda actual.
                # -----------------------------------------------------
                if is_rock:
                    continue

                left_entry = frontier[column - 1] if column > 0 else 0

                upper_right_selected = (
                    column + 1 < columns and frontier[column + 1] != 0
                )

                # Un contacto diagonal es válido en un giro local si
                # existe una celda puente ortogonal. Para la diagonal
                # superior izquierda, ambos posibles puentes ya se conocen.
                if upper_left_selected and not upper_entry and not left_entry:
                    continue

                # Si existe canal en la diagonal superior derecha y no en
                # la celda superior, la celda derecha deberá seleccionarse
                # para completar un giro válido.
                must_select_next = upper_right_selected and not upper_entry

                current_degree = int(bool(upper_entry)) + int(bool(left_entry))
                current_limit = 1 if is_required else 2

                if current_degree > current_limit:
                    continue

                new_frontier = list(frontier)
                valid = True

                upper_label = None
                left_label = None
                upper_final_degree = None

                # La nueva celda se conecta con la celda de la izquierda.
                if left_entry:
                    left_label = entry_label(left_entry)
                    left_degree = entry_degree(left_entry) + 1

                    left_is_start = row == 0 and column - 1 == 0
                    left_limit = 1 if left_is_start else 2

                    if left_degree > left_limit:
                        valid = False
                    else:
                        new_frontier[column - 1] = encode_entry(
                            left_label,
                            left_degree,
                        )

                if not valid:
                    continue

                # También se conecta con la celda situada arriba.
                if upper_entry:
                    upper_label = entry_label(upper_entry)
                    upper_final_degree = entry_degree(upper_entry) + 1

                    upper_is_start = row - 1 == 0 and column == 0
                    upper_limit = 1 if upper_is_start else 2

                    if upper_final_degree > upper_limit:
                        continue

                # Determinamos la componente de la nueva celda.
                if upper_entry and left_entry:
                    # Unir dos puntos de la misma componente cerraría
                    # un ciclo, lo cual no es un canal válido.
                    if upper_label == left_label:
                        continue

                    kept_label = min(upper_label, left_label)
                    removed_label = max(upper_label, left_label)

                    # Fusionamos las dos componentes en toda la frontera.
                    for index, entry in enumerate(new_frontier):
                        if entry and entry_label(entry) == removed_label:
                            new_frontier[index] = encode_entry(
                                kept_label,
                                entry_degree(entry),
                            )

                    current_label = kept_label

                elif upper_entry:
                    current_label = upper_label

                elif left_entry:
                    current_label = left_label

                else:
                    # Comienza una nueva componente parcial.
                    greatest_label = max(
                        (entry_label(entry) for entry in new_frontier if entry),
                        default=0,
                    )
                    current_label = greatest_label + 1

                # La posición de la celda superior es reemplazada por la
                # nueva celda de la fila actual.
                new_frontier[column] = encode_entry(
                    current_label,
                    current_degree,
                )

                # La celda superior abandona la frontera. Su grado ya debe
                # ser definitivo y correcto.
                if upper_entry:
                    expected_degree = 1 if row - 1 == 0 and column == 0 else 2

                    if upper_final_degree != expected_degree:
                        continue

                    # Buscamos la etiqueta que quedó después de una posible
                    # fusión de componentes.
                    surviving_label = upper_label

                    if upper_entry and left_entry:
                        surviving_label = current_label

                    component_survives = any(
                        entry and entry_label(entry) == surviving_label
                        for entry in new_frontier
                    )

                    if not component_survives:
                        continue

                normalized = normalize_frontier(tuple(new_frontier))
                if column == columns - 1:
                    must_select_next = False

                key = (
                    normalized,
                    next_upper_left,
                    must_select_next,
                )

                cell_index = row * columns + column
                new_mask = channel_mask | (1 << cell_index)

                save_best(
                    next_states,
                    key,
                    length + 1,
                    new_mask,
                )

            states = next_states

    best_length = -1
    best_mask = 0

    # Al terminar, las entradas de la frontera pertenecen a la última
    # fila. Ninguna puede recibir conexiones adicionales.
    for state, value in states.items():
        frontier, upper_left_selected, must_select_current = state
        length, channel_mask = value
        labels = set()
        valid = True

        for column, entry in enumerate(frontier):
            if entry == 0:
                continue

            expected_degree = 1 if column == columns - 1 else 2

            if entry_degree(entry) != expected_degree:
                valid = False
                break

            labels.add(entry_label(entry))

        # Debe quedar exactamente una componente y la salida debe estar
        # seleccionada en la última columna.
        if not valid or len(labels) != 1 or frontier[-1] == 0:
            continue

        if length > best_length:
            best_length = length
            best_mask = channel_mask

    return best_mask


def build_output(field, channel_mask):
    """Construye las filas de salida usando la máscara calculada."""

    rows = len(field)
    columns = len(field[0])
    result = []

    for row in range(rows):
        output_row = []

        for column in range(columns):
            cell_index = row * columns + column

            if channel_mask & (1 << cell_index):
                output_row.append("C")
            else:
                output_row.append(field[row][column])

        result.append("".join(output_row))

    return result


def solve():
    input_stream = sys.stdin.buffer
    output = []
    case_number = 1

    while True:
        line = input_stream.readline()

        if not line:
            break

        if not line.strip():
            continue

        rows, columns = map(int, line.split())

        if rows == 0 and columns == 0:
            break

        field = [input_stream.readline().decode().strip() for _ in range(rows)]

        channel_mask = longest_channel(field)
        solved_field = build_output(field, channel_mask)

        output.append(f"Case {case_number}:")
        output.extend(solved_field)
        output.append("")
        case_number += 1

    print("\n".join(output))


if __name__ == "__main__":
    solve()
