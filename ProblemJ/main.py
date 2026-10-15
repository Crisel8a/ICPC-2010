"""
Sharing Chocolate

Determina si una barra rectangular puede dividirse, mediante cortes completos
horizontales o verticales, en rectángulos con las áreas solicitadas.

La solución utiliza programación dinámica, bitmasks y memoización.
"""

import sys
from functools import cache


def se_puede_dividir(cantidad, ancho, alto, porciones):
    """Retorna True si la barra puede dividirse como se solicita."""

    area_barra = ancho * alto

    # Todo el chocolate debe repartirse, sin que sobre ni falte ninguna pieza.
    if sum(porciones) != area_barra:
        return False

    # ------------------------------------------------------------------
    # 1. Precalcular el área de cada subconjunto de amigos.
    # ------------------------------------------------------------------
    # El bit i de una máscara indica si la porción i está incluida.
    # Ejemplo: 0101 contiene las porciones 0 y 2.
    total_mascaras = 1 << cantidad
    area = [0] * total_mascaras

    for mascara in range(1, total_mascaras):
        # Aislamos el bit menos significativo encendido.
        ultimo_bit = mascara & -mascara

        # bit_length() - 1 convierte ese bit en su índice.
        indice = ultimo_bit.bit_length() - 1

        # Quitamos el bit y reutilizamos una suma ya calculada.
        mascara_sin_bit = mascara ^ ultimo_bit
        area[mascara] = area[mascara_sin_bit] + porciones[indice]

    @cache
    def resolver(mascara, lado_1):
        """
        Indica si las porciones de 'mascara' caben en un rectángulo.

        Solo guardamos un lado del rectángulo. El otro se obtiene dividiendo
        el área total del subconjunto entre ese lado.
        """
        area_actual = area[mascara]

        # El segundo lado debe ser entero, porque la barra está formada por
        # piezas completas.
        if area_actual % lado_1 != 0:
            return False

        lado_2 = area_actual // lado_1

        # Un rectángulo a × b es equivalente a uno b × a. Normalizamos la
        # orientación para reducir estados duplicados en la memoización.
        if lado_1 > lado_2:
            return resolver(mascara, lado_2)

        ancho_actual = lado_1
        alto_actual = lado_2

        # Caso base: si solo queda una porción, entregamos todo el rectángulo
        # actual a ese amigo. No hace falta realizar otro corte.
        if mascara & (mascara - 1) == 0:
            return True

        # ------------------------------------------------------------------
        # 2. Probar todos los posibles primeros cortes.
        # ------------------------------------------------------------------
        # Un primer corte separa las porciones en dos grupos no vacíos.
        # Para evitar probar A|B y luego B|A, exigimos que el primer grupo
        # contenga el bit fijo más pequeño de la máscara.
        bit_fijo = mascara & -mascara
        submascara = (mascara - 1) & mascara

        while submascara:
            if submascara & bit_fijo:
                otra_mascara = mascara ^ submascara
                area_primera = area[submascara]

                # ------------------------------------------------------
                # Opción A: corte horizontal.
                # ------------------------------------------------------
                # Las dos partes conservan el mismo ancho. El área del
                # primer grupo debe ocupar una cantidad entera de filas.
                if area_primera % ancho_actual == 0:
                    alto_primera = area_primera // ancho_actual

                    if 0 < alto_primera < alto_actual:
                        if resolver(submascara, ancho_actual) and resolver(
                            otra_mascara, ancho_actual
                        ):
                            return True

                # ------------------------------------------------------
                # Opción B: corte vertical.
                # ------------------------------------------------------
                # Las dos partes conservan la misma altura. El área del
                # primer grupo debe ocupar una cantidad entera de columnas.
                if area_primera % alto_actual == 0:
                    ancho_primera = area_primera // alto_actual

                    if 0 < ancho_primera < ancho_actual:
                        if resolver(submascara, ancho_primera) and resolver(
                            otra_mascara,
                            ancho_actual - ancho_primera,
                        ):
                            return True

            # Genera el siguiente subconjunto de 'mascara'.
            submascara = (submascara - 1) & mascara

        # Ninguna separación produjo dos rectángulos válidos.
        return False

    mascara_completa = (1 << cantidad) - 1
    return resolver(mascara_completa, ancho)


def main():
    """Lee todos los casos de prueba e imprime las respuestas."""
    datos = list(map(int, sys.stdin.buffer.read().split()))
    posicion = 0
    numero_caso = 1
    salida = []

    while posicion < len(datos):
        cantidad = datos[posicion]
        posicion += 1

        # Un cero indica el final de toda la entrada.
        if cantidad == 0:
            break

        ancho = datos[posicion]
        alto = datos[posicion + 1]
        posicion += 2

        porciones = datos[posicion : posicion + cantidad]
        posicion += cantidad

        posible = se_puede_dividir(cantidad, ancho, alto, porciones)
        respuesta = "Yes" if posible else "No"
        salida.append(f"Case {numero_caso}: {respuesta}")

        numero_caso += 1

    print("\n".join(salida))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# EJEMPLO DE USO
# ---------------------------------------------------------------------------
#
# Entrada:
#
# 4
# 3 4
# 6 3 2 1
# 2
# 3 3
# 1 5
# 0
#
# Output esperado:
#
# Case 1: Yes
# Case 2: No
#
# Explicación:
#   * La primera barra tiene 12 piezas y puede dividirse en rectángulos de
#     áreas 6, 3, 2 y 1.
#   * La segunda barra tiene 9 piezas, pero las solicitudes solo suman 6;
#     sobraría chocolate y por eso la respuesta es No.
