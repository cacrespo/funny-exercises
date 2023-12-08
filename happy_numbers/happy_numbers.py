"""
Script para generar "happy numbers".

Este script retorna una cantidad especifica de "happy numbers"[1] encontrados
en un rango de valores determinado vía parámetros.
Se puede establecer valor final y potencia para realizar los cálculos, así como
el rango de valores a revisar.

Parámetros
----------
resultados : int
    Cantidad requerida de números felices.

valor_final : int [optional, default=1]
    Valor final para definir si un número es feliz.

potencia : [optional, default=2]
    Valor al cuál se eleva cada uno de los dígitos.

rango_inicio : [optional, default=1]
    Valor inicial del rango que se evalúa para determinar los números felices.

rango_fin : [optional, default=1000]
    Valor final del rango que se evalúa para determinar los números felices.


1_ https://en.wikipedia.org/wiki/Happy_number
"""

import sys


def es_numero_feliz(x: int, potencia: int, numero_final: int) -> bool:
    """Verifica si un número es feliz."""
    historial = set()

    while x != numero_final and x not in historial:
        historial.add(x)
        x = sum(int(n) ** potencia for n in str(x))

    return x == numero_final


def listar_numero_felices(
    cantidad: int,
    potencia: int = 2,
    numero_final: int = 1,
    init: int = 1,
    end: int = 1000
) -> list[int]:
    """Genera una lista de números felices."""
    happy_numbers = []
    numero = init

    while len(happy_numbers) < cantidad and numero <= end:
        if es_numero_feliz(numero, potencia, numero_final):
            happy_numbers.append(numero)
        numero += 1

    return happy_numbers


if __name__ == "__main__":
    cantidad, *args = sys.argv[1:]
    resultado = listar_numero_felices(int(cantidad), *[int(i) for i in args])

    # está medio feo pero es para levantar los argumentos utilizados
    args = args + [2, 1, 1, 1000][- (4 - len(args)):]

    print(f"""
    Los primeros {cantidad} números felices en el rango seleccionado son:
    {resultado}

    Argumentos utilizados
    Potencia: {args[0]}
    Número final: {args[1]}
    Rango inicio: {args[2]}
    Rango final: {args[3]}
    """)
