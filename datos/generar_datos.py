"""
Generador de datos de prueba - Taller de Ordenamiento y Búsqueda.

Se ejecuta UNA sola vez. Produce, para cada tamaño n:
  - n_<n>_aleatorio.txt    enteros aleatorios de 8 dígitos [10.000.000, 99.999.999]
  - n_<n>_ascendente.txt   los mismos datos ordenados ascendentemente
  - n_<n>_descendente.txt  los mismos datos ordenados descendentemente
  - claves_n_<n>.txt       1.000 claves de búsqueda: 500 presentes y 500 ausentes (barajadas)

Semilla fija (SEMILLA) para que cualquiera pueda regenerar exactamente los mismos archivos.
Uso:  python3 generar_datos.py   (escribe en la carpeta donde está este script)
"""
import os
import random

SEMILLA = 2026
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
MINIMO, MAXIMO = 10_000_000, 99_999_999
CLAVES_PRESENTES, CLAVES_AUSENTES = 500, 500

CARPETA = os.path.dirname(os.path.abspath(__file__))


def escribir(nombre, valores):
    with open(os.path.join(CARPETA, nombre), "w") as f:
        f.write("\n".join(map(str, valores)))
        f.write("\n")


def main():
    rng = random.Random(SEMILLA)
    for n in TAMANOS:
        datos = [rng.randint(MINIMO, MAXIMO) for _ in range(n)]
        ascendente = sorted(datos)
        descendente = ascendente[::-1]
        escribir(f"n_{n}_aleatorio.txt", datos)
        escribir(f"n_{n}_ascendente.txt", ascendente)
        escribir(f"n_{n}_descendente.txt", descendente)

        # Claves de búsqueda: 500 tomadas de posiciones distintas del arreglo
        # y 500 números de 8 dígitos que NO están en el arreglo.
        conjunto = set(datos)
        presentes = [datos[i] for i in rng.sample(range(n), CLAVES_PRESENTES)]
        ausentes = set()
        while len(ausentes) < CLAVES_AUSENTES:
            x = rng.randint(MINIMO, MAXIMO)
            if x not in conjunto:
                ausentes.add(x)
        claves = presentes + sorted(ausentes)
        rng.shuffle(claves)
        escribir(f"claves_n_{n}.txt", claves)

        repetidos = n - len(conjunto)
        print(f"n={n:>9,}: generado (valores repetidos en el arreglo: {repetidos})")


if __name__ == "__main__":
    main()
