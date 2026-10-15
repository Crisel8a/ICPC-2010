"""
Lakes in a Triangulated Landscape

La solución procesa el terreno desde las alturas más bajas hacia las más
altas. Union-Find mantiene las regiones que ya quedaron por debajo del nivel
actual del agua.

Si una región atrapada alcanza por primera vez una región conectada con el
borde a la altura H, entonces se formó un lago cuyo nivel final es H.
"""

import sys
from math import atan2


class UnionFind:
    """Mantiene componentes conectados y si cada uno puede drenar."""

    def __init__(self, cantidad):
        self.padre = list(range(cantidad))
        self.tamano = [1] * cantidad
        self.drena = [False] * cantidad

    def encontrar(self, x):
        """Devuelve el representante del componente de x."""
        if self.padre[x] != x:
            # Compresión de caminos: acelera las próximas búsquedas.
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def unir(self, a, b):
        """Une los componentes de a y b y devuelve su representante."""
        raiz_a = self.encontrar(a)
        raiz_b = self.encontrar(b)

        if raiz_a == raiz_b:
            return raiz_a

        # Colocamos el árbol pequeño debajo del grande.
        if self.tamano[raiz_a] < self.tamano[raiz_b]:
            raiz_a, raiz_b = raiz_b, raiz_a

        self.padre[raiz_b] = raiz_a
        self.tamano[raiz_a] += self.tamano[raiz_b]

        # El componente unido drena si cualquiera de los dos ya drenaba.
        self.drena[raiz_a] = self.drena[raiz_a] or self.drena[raiz_b]
        return raiz_a


def encontrar_vertices_del_borde(coordenadas, vecinos):
    """
    Encuentra los vértices de la cara exterior del dibujo plano.

    Para recorrer una cara, avanzamos por lados dirigidos y, al llegar a un
    vértice, tomamos el vecino inmediatamente anterior en orden antihorario.
    Así mantenemos la misma cara a nuestra izquierda.
    """
    cantidad = len(coordenadas)

    # Ordenamos los vecinos por el ángulo que forman alrededor de cada punto.
    ordenados = []
    posicion = []

    for u in range(cantidad):
        x_u, y_u = coordenadas[u]

        lista = sorted(
            vecinos[u],
            key=lambda v: atan2(
                coordenadas[v][1] - y_u,
                coordenadas[v][0] - x_u,
            ),
        )

        ordenados.append(lista)
        posicion.append({v: i for i, v in enumerate(lista)})

    lados_dirigidos_visitados = set()
    cara_exterior = []
    menor_area_doble = None

    # Cada lado no dirigido aparece dos veces: u -> v y v -> u.
    for u in range(cantidad):
        for v in ordenados[u]:
            if (u, v) in lados_dirigidos_visitados:
                continue

            cara = []
            actual, siguiente = u, v

            # La regla de avance define una permutación de los semilados.
            # Por eso volveremos al semilado inicial y cerraremos la cara.
            while (actual, siguiente) not in lados_dirigidos_visitados:
                lados_dirigidos_visitados.add((actual, siguiente))
                cara.append(actual)

                indice_de_actual = posicion[siguiente][actual]
                nuevo_siguiente = ordenados[siguiente][
                    (indice_de_actual - 1) % len(ordenados[siguiente])
                ]
                actual, siguiente = siguiente, nuevo_siguiente

            # Fórmula del zapatero. No dividimos entre dos porque únicamente
            # necesitamos comparar el signo y el tamaño de las áreas.
            area_doble = 0
            for i in range(len(cara)):
                a = cara[i]
                b = cara[(i + 1) % len(cara)]
                x_a, y_a = coordenadas[a]
                x_b, y_b = coordenadas[b]
                area_doble += x_a * y_b - x_b * y_a

            # Con este sentido de recorrido, las caras interiores tienen área
            # positiva y la cara exterior tiene área negativa.
            if menor_area_doble is None or area_doble < menor_area_doble:
                menor_area_doble = area_doble
                cara_exterior = cara

    return set(cara_exterior)


def resolver_caso(coordenadas, alturas, lados, vecinos):
    """Calcula y devuelve, ordenados, los niveles de todos los lagos."""
    cantidad = len(coordenadas)
    vertices_del_borde = encontrar_vertices_del_borde(coordenadas, vecinos)

    # Agrupamos los vértices por altura. Los de igual altura deben procesarse
    # simultáneamente para tratar correctamente los contactos de profundidad 0.
    por_altura = {}
    for vertice, altura in enumerate(alturas):
        por_altura.setdefault(altura, []).append(vertice)

    union_find = UnionFind(cantidad)
    activo = [False] * cantidad
    niveles_de_lagos = []

    for altura in sorted(por_altura):
        nuevos = por_altura[altura]

        # ---------------------------------------------------------------
        # 1. Construimos un Union-Find temporal para este nivel.
        # ---------------------------------------------------------------
        # Sus nodos serán:
        #   ("nuevo", v): un vértice que aparece en esta altura.
        #   ("viejo", r): un componente de menor altura, representado por r.
        nodos_temporales = []
        indice_temporal = {}

        def obtener_indice(clave):
            """Crea un nodo temporal solo si todavía no existe."""
            if clave not in indice_temporal:
                indice_temporal[clave] = len(nodos_temporales)
                nodos_temporales.append(clave)
            return indice_temporal[clave]

        for v in nuevos:
            obtener_indice(("nuevo", v))

        # Primero descubrimos todos los componentes viejos adyacentes.
        for v in nuevos:
            for vecino in vecinos[v]:
                if activo[vecino]:
                    raiz = union_find.encontrar(vecino)
                    obtener_indice(("viejo", raiz))

        temporal = UnionFind(len(nodos_temporales))

        # Conectamos los elementos que participan en el mismo evento de altura.
        for v in nuevos:
            nodo_v = obtener_indice(("nuevo", v))

            for vecino in vecinos[v]:
                if activo[vecino]:
                    raiz = union_find.encontrar(vecino)
                    nodo_raiz = obtener_indice(("viejo", raiz))
                    temporal.unir(nodo_v, nodo_raiz)

                elif alturas[vecino] == altura:
                    nodo_vecino = obtener_indice(("nuevo", vecino))
                    temporal.unir(nodo_v, nodo_vecino)

        # Reunimos la información de cada evento temporal.
        eventos = {}

        for indice, (tipo, valor) in enumerate(nodos_temporales):
            raiz_evento = temporal.encontrar(indice)
            evento = eventos.setdefault(
                raiz_evento,
                {
                    "toca_borde": False,
                    "componentes_viejos": set(),
                },
            )

            if tipo == "nuevo":
                if valor in vertices_del_borde:
                    evento["toca_borde"] = True
            else:
                evento["componentes_viejos"].add(valor)

        # ---------------------------------------------------------------
        # 2. Decidimos qué depresiones se desbordan en esta altura.
        # ---------------------------------------------------------------
        for evento in eventos.values():
            raices_viejas = evento["componentes_viejos"]

            drena = evento["toca_borde"] or any(
                union_find.drena[union_find.encontrar(raiz)] for raiz in raices_viejas
            )

            if drena:
                # Cada componente que estaba atrapado justo antes de alcanzar
                # esta altura corresponde a un lago distinto.
                for raiz in raices_viejas:
                    raiz = union_find.encontrar(raiz)
                    if not union_find.drena[raiz]:
                        niveles_de_lagos.append(altura)

        # ---------------------------------------------------------------
        # 3. Activamos el nivel y hacemos permanentes sus conexiones.
        # ---------------------------------------------------------------
        for v in nuevos:
            activo[v] = True
            union_find.padre[v] = v
            union_find.tamano[v] = 1
            union_find.drena[v] = v in vertices_del_borde

        for v in nuevos:
            for vecino in vecinos[v]:
                if activo[vecino]:
                    union_find.unir(v, vecino)

    niveles_de_lagos.sort()
    return niveles_de_lagos


def main():
    """Lee todos los casos, los resuelve e imprime el formato solicitado."""
    datos = sys.stdin.buffer.read().split()
    posicion = 0
    numero_de_caso = 1
    salida = []

    while posicion < len(datos):
        cantidad_puntos = int(datos[posicion])
        cantidad_lados = int(datos[posicion + 1])
        posicion += 2

        if cantidad_puntos == 0 and cantidad_lados == 0:
            break

        coordenadas = [None] * cantidad_puntos
        alturas = [0] * cantidad_puntos
        codigo_a_indice = {}

        for i in range(cantidad_puntos):
            codigo = datos[posicion].decode()
            x = int(datos[posicion + 1])
            y = int(datos[posicion + 2])
            h = int(datos[posicion + 3])
            posicion += 4

            codigo_a_indice[codigo] = i
            coordenadas[i] = (x, y)
            alturas[i] = h

        lados = []
        vecinos = [[] for _ in range(cantidad_puntos)]

        for _ in range(cantidad_lados):
            codigo_a = datos[posicion].decode()
            codigo_b = datos[posicion + 1].decode()
            posicion += 2

            a = codigo_a_indice[codigo_a]
            b = codigo_a_indice[codigo_b]
            lados.append((a, b))
            vecinos[a].append(b)
            vecinos[b].append(a)

        niveles = resolver_caso(coordenadas, alturas, lados, vecinos)

        salida.append(f"Case {numero_de_caso}:")
        if niveles:
            salida.extend(f"  {nivel}" for nivel in niveles)
        else:
            salida.append("  0")

        numero_de_caso += 1

    print("\n".join(salida))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# EJEMPLO DE USO
# ---------------------------------------------------------------------------
#
# Guarda este archivo como solucion.py y ejecútalo proporcionando la entrada
# estándar. Por ejemplo:
#
# Entrada:
#
# 7 12
# aa 1 1 5
# bb 1 3 5
# xX 0 2 10
# XY 0 4 15
# XZ 3 4 11
# xy 0 0 15
# xz 3 0 15
# xX XZ
# XY XZ
# xX XY
# xX xy
# xX xz
# xz xy
# aa xX
# aa xy
# aa xz
# bb xX
# bb XY
# bb XZ
# 0 0
#
# Salida esperada:
#
# Case 1:
#   10
#   10
#
# Explicación: aa y bb son dos depresiones diferentes. Las dos alcanzan una
# salida cuando el agua llega al nivel 10. Como solo se tocan con profundidad
# cero, se imprimen dos lagos, aunque tengan el mismo nivel.
