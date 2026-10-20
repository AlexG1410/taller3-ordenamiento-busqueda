"""Utilidades comunes de los programas de medición (lectura de datos, estadística, CSV)."""
import math
import os


def leer_enteros(ruta):
    with open(ruta) as f:
        return [int(linea) for linea in f if linea.strip()]


def promedio(v):
    return sum(v) / len(v)


def desviacion(v):
    """Desviación estándar muestral (divide entre n - 1)."""
    m = promedio(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def num(x):
    return f"{x:.6f}"


def texto(s):
    return '"' + s.replace('"', "'") + '"'


def agregar_fila(csv, cabecera, fila):
    nuevo = not os.path.exists(csv)
    carpeta = os.path.dirname(csv)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(csv, "a", encoding="utf-8") as f:
        if nuevo:
            f.write(cabecera + "\n")
        f.write(fila + "\n")
