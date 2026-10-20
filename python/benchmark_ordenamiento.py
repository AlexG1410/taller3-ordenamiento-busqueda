"""
Medición de los algoritmos de ordenamiento (Punto 1) en Python (lenguaje interpretado).

Uso: python3 python/benchmark_ordenamiento.py <algoritmo> <carpeta_datos> <archivo_csv>
     algoritmo: insertion | dualpivot | merge | heap | radix | bucket

Mismo protocolo que la versión Java (BenchmarkOrdenamiento.java), excepto que CPython
interpreta bytecode y no tiene compilación JIT, por lo que no hay ejecución de calentamiento.
Tiempo con time.perf_counter_ns(); copia nueva por repetición; verificación fuera del tiempo;
regla de 5 minutos; los errores (RecursionError) se registran y el tiempo se estima.
No se modifica el límite de recursión de Python (1000 por defecto).
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ordenamiento as o  # noqa: E402
from utilidades import leer_enteros, promedio, desviacion, num, texto, agregar_fila  # noqa: E402

TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
VARIANTES = ["aleatorio", "ascendente", "descendente"]
REPETICIONES = 5
LIMITE_MS = 5 * 60 * 1000.0
CABECERA = ("algoritmo,lenguaje,variante,n,rep1_ms,rep2_ms,rep3_ms,rep4_ms,rep5_ms,"
            "promedio_ms,desviacion_ms,tipo,observacion")

ALGORITMOS = {
    "insertion": ("Insertion Sort", o.insertion_sort),
    "dualpivot": ("Dual-Pivot QuickSort", o.dual_pivot_quick_sort),
    "merge": ("Merge Sort", o.merge_sort),
    "heap": ("Heap Sort", o.heap_sort),
    "radix": ("Radix Sort", o.radix_sort),
    "bucket": ("Bucket Sort", o.bucket_sort),
}


def complejidad(alg, variante, n):
    """Función de crecimiento teórica del caso que corresponde a cada variante de entrada."""
    lg = math.log2(n)
    if alg == "insertion":
        return n if variante == "ascendente" else n * n
    if alg == "dualpivot":
        return n * lg if variante == "aleatorio" else n * n
    if alg in ("merge", "heap"):
        return n * lg
    return n  # radix (d = 8 fijo) y bucket (distribución uniforme)


def nombre_modelo(alg, variante):
    r = complejidad(alg, variante, 10_000) / complejidad(alg, variante, 1_000)
    return "O(n^2)" if r > 50 else ("O(n log n)" if r > 11 else "O(n)")


def escribir_estimado(csv, nombre, variante, n, estimado, obs):
    fila = f"{nombre},Python,{variante},{n},,,,,,{num(estimado)},,estimado,{texto(obs)}"
    agregar_fila(csv, CABECERA, fila)
    print(f"{nombre:<22} {variante:<12} n={n:<8} ESTIMADO={estimado:12.3f} ms  ({obs})", flush=True)


def main():
    clave, datos, csv = sys.argv[1], sys.argv[2], sys.argv[3]
    nombre, algoritmo = ALGORITMOS[clave]

    for variante in VARIANTES:
        n_ref, t_ref = -1, -1.0
        for n in TAMANOS:
            original = leer_enteros(os.path.join(datos, f"n_{n}_{variante}.txt"))
            referencia = leer_enteros(os.path.join(datos, f"n_{n}_ascendente.txt"))
            modelo = nombre_modelo(clave, variante)
            factor = complejidad(clave, variante, n) / complejidad(clave, variante, n_ref) if n_ref > 0 else -1
            previsto = t_ref * factor if n_ref > 0 else -1
            base = (f"{modelo} a partir de n={n_ref} (t={t_ref:.3f} ms x {factor:.2f})"
                    if n_ref > 0 else "sin tamaño menor medido")

            if previsto > LIMITE_MS:
                escribir_estimado(csv, nombre, variante, n, previsto,
                                  f"No ejecutado: tiempo previsto {previsto / 1000:.1f} s > 5 min. "
                                  f"Estimado con {base}")
                continue

            reps = []
            fallo = None
            excedido = None
            for _ in range(REPETICIONES):
                copia = original[:]                       # copia nueva, fuera del tiempo medido
                try:
                    a = time.perf_counter_ns()
                    algoritmo(copia)
                    b = time.perf_counter_ns()
                except RecursionError as e:
                    fallo = e
                    break
                if copia != referencia:                   # verificación fuera del tiempo medido
                    raise RuntimeError(f"Resultado incorrecto: {nombre} {variante} n={n}")
                t = (b - a) / 1e6
                if t > LIMITE_MS:
                    excedido = t
                    break
                reps.append(t)

            if fallo is not None:
                escribir_estimado(csv, nombre, variante, n, previsto,
                                  f"Falla: RecursionError ('{fallo}'); el límite de recursión de "
                                  f"Python es {sys.getrecursionlimit()}. Estimado con {base}")
                continue
            if excedido is not None:
                escribir_estimado(csv, nombre, variante, n, previsto if previsto > 0 else excedido,
                                  f"Una ejecución tardó {excedido / 1000:.1f} s > 5 min; no se repitió. "
                                  f"Estimado con {base}")
                continue

            prom, desv = promedio(reps), desviacion(reps)
            fila = (f"{nombre},Python,{variante},{n}," + ",".join(num(t) for t in reps)
                    + f",{num(prom)},{num(desv)},medido,{texto('Sin calentamiento (CPython no usa JIT). Verificado OK')}")
            agregar_fila(csv, CABECERA, fila)
            print(f"{nombre:<22} {variante:<12} n={n:<8} prom={prom:12.3f} ms  desv={desv:10.3f} ms", flush=True)
            n_ref, t_ref = n, prom


if __name__ == "__main__":
    main()
