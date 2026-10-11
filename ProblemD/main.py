"""
Conquista de castillos - DP sobre árboles.

Ejemplo de entrada:

3
5 5 5
10 5 5
5 1 1
1 3
2 3
5
10 5 10
20 10 5
10 10 5
5 5 5
20 0 10
1 2
1 3
1 4
3 5
0

Salida correspondiente:

Case 1: 22
Case 2: 65
"""

import sys


def minimum_army(castles, graph):
    """Devuelve el ejército mínimo para conquistar todo el árbol."""

    castle_count = len(castles)

    def summarize_subtree(node, parent):
        """
        Devuelve (need, loss) para el subárbol de node.

        need: soldados mínimos al comenzar este subárbol.
        loss: soldados que ya no estarán disponibles al terminarlo.
        """

        attack, deaths, guards = castles[node]

        # Al conquistar este castillo, los muertos y los guardias dejan
        # de formar parte del ejército móvil.
        current_loss = deaths + guards

        # Debemos cumplir el requisito del ataque y, además, tener
        # suficientes soldados para cubrir deaths + guards.
        current_need = max(attack, current_loss)

        children = []

        for neighbor in graph[node]:
            if neighbor == parent:
                continue

            child_need, child_loss = summarize_subtree(neighbor, node)
            children.append((child_need, child_loss))

        # Un subárbol con need - loss grande debe conquistarse antes.
        # Es el que necesita conservar más soldados por encima de lo
        # que consumirá durante su propia conquista.
        children.sort(
            key=lambda summary: summary[0] - summary[1],
            reverse=True,
        )

        # Combinamos el castillo actual con sus subárboles, en el orden
        # óptimo calculado arriba.
        for child_need, child_loss in children:
            # Antes de comenzar el hijo ya hemos perdido current_loss.
            # Por eso el ejército inicial debe cubrir ambos valores.
            current_need = max(
                current_need,
                current_loss + child_need,
            )

            current_loss += child_loss

        return current_need, current_loss

    answer = float("inf")

    # El ejército puede comenzar en cualquier castillo. Enraizamos el
    # árbol en cada posibilidad y conservamos el mejor resultado.
    for root in range(castle_count):
        required, total_loss = summarize_subtree(root, -1)
        answer = min(answer, required)

    return answer


def solve():
    input_stream = sys.stdin.buffer
    answers = []
    case_number = 1

    while True:
        line = input_stream.readline()

        if not line:
            break

        if not line.strip():
            continue

        castle_count = int(line)

        if castle_count == 0:
            break

        castles = []

        # Los castillos se reciben en orden, del 1 al n.
        for _ in range(castle_count):
            attack, deaths, guards = map(
                int,
                input_stream.readline().split(),
            )
            castles.append((attack, deaths, guards))

        # Como la región es un árbol, tiene exactamente n - 1 rutas.
        graph = [[] for _ in range(castle_count)]

        for _ in range(castle_count - 1):
            first, second = map(
                int,
                input_stream.readline().split(),
            )

            # Convertimos la numeración 1..n a índices 0..n-1.
            first -= 1
            second -= 1

            graph[first].append(second)
            graph[second].append(first)

        result = minimum_army(castles, graph)
        answers.append(f"Case {case_number}: {result}")
        case_number += 1

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
