"""
Bleatrix Trotter the sheep has devised a strategy that helps her fall asleep
faster. First, she picks a number N. Then she starts naming N, 2 × N, 3 × N,
and so on. Whenever she names a number, she thinks about all of the digits in
that number. She keeps track of which digits (0, 1, 2, 3, 4, 5, 6, 7, 8, and 9)
she has seen at least once so far as part of any number she has named. Once she
has seen each of the ten digits at least once, she will fall asleep.
Bleatrix must start with N and must always name (i + 1) × N directly after
i × N.

Usage:
    python beatrix_trotter.py INPUT_FILE(s)

"""


import sys


def open_file(file: str) -> list:
    try:
        values = [int(w.rstrip()) for w in open(file)]
    except Exception as e:
        print(f"No se ha podido procesar el archivo {file}: {e}\n---")
    else:
        print(f"[{file}] processed!")
        file_ok = True
        if values[0] != len(values[1:]):
            print("problems: Test cases (T) != Total cases given (N)\n---")
            file_ok = False
        if len(values[1:]) not in range(1, 101):
            print("problems: Not 1 <= Test cases (T) <= 100\n---")
            file_ok = False

        return values[1:] if file_ok else None


def es_numero_dormir(n: int):
    """Retorna el valor fall asleep"""
    historial = set()
    multiplier = 0

    if n == 0:
        return 'INSOMIA'

    if n not in range(201):
        return f"N={n} INVALID (0 <= N <= 200)"

    while len(historial) < 10:
        multiplier += 1
        current_number = multiplier * n
        historial.update(str(current_number))

    return current_number


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        values = open_file(arg)
        if not (values is None):
            for n, value in enumerate(values):
                print(f"Case #{n+1}: {es_numero_dormir(value)}")
            print("---")
