"""
Medición de los algoritmos de búsqueda (Punto 2) en Python (lenguaje interpretado).

Uso: python3 python/benchmark_busqueda.py <algoritmo> <carpeta_datos> <archivo_csv>
     algoritmo: lineal | binaria | ternaria | saltos | interpolacion | exponencial

Mismo protocolo que BenchmarkBusqueda.java (sin calentamiento: CPython no usa JIT).
Se mide el tiempo total del lote de 1.000 búsquedas y se reporta el promedio por búsqueda.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import busqueda as bq  # noqa: E402
from utilidades import leer_enteros, promedio, desviacion, num, texto, agregar_fila  # noqa: E402

TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
REPETICIONES = 5
BUSQUEDAS = 1_000
CABECERA = ("algoritmo,lenguaje,variante,n,rep1_ns,rep2_ns,rep3_ns,rep4_ns,rep5_ns,"
            "promedio_ns,desviacion_ns,tipo,observacion")

ALGORITMOS = {
    "lineal": ("Búsqueda Lineal", bq.linear_search),
    "binaria": ("Búsqueda Binaria", bq.binary_search),
    "ternaria": ("Búsqueda Ternaria", bq.ternary_search),
    "saltos": ("Búsqueda por Saltos", bq.jump_search),
    "interpolacion": ("Búsqueda por Interpolación", bq.interpolation_search),
    "exponencial": ("Búsqueda Exponencial", bq.exponential_search),
}


def main():
    clave, datos, csv = sys.argv[1], sys.argv[2], sys.argv[3]
    nombre, buscar = ALGORITMOS[clave]

    for n in TAMANOS:
        arr = leer_enteros(os.path.join(datos, f"n_{n}_ascendente.txt"))
        claves = leer_enteros(os.path.join(datos, f"claves_n_{n}.txt"))
        conjunto = set(arr)
        lotes = {
            "claves_mixtas": claves,
            "pos_inicio": [arr[0]] * BUSQUEDAS,
            "pos_centro": [arr[(n - 1) // 2]] * BUSQUEDAS,
            "pos_final": [arr[n - 1]] * BUSQUEDAS,
        }
        for variante, lote in lotes.items():
            # Verificación de corrección (fuera del tiempo medido)
            for x in lote:
                idx = buscar(arr, x)
                ok = (idx >= 0 and arr[idx] == x) if x in conjunto else idx == -1
                if not ok:
                    raise RuntimeError(f"Resultado incorrecto: {nombre} n={n} x={x}")

            reps = []
            for _ in range(REPETICIONES):
                a = time.perf_counter_ns()
                for x in lote:
                    buscar(arr, x)
                b = time.perf_counter_ns()
                reps.append((b - a) / BUSQUEDAS)          # ns promedio por búsqueda
            prom, desv = promedio(reps), desviacion(reps)
            obs = "Tiempo por búsqueda = tiempo total de 1000 búsquedas / 1000. Sin calentamiento (sin JIT). Verificado OK"
            fila = (f"{nombre},Python,{variante},{n}," + ",".join(num(t) for t in reps)
                    + f",{num(prom)},{num(desv)},medido,{texto(obs)}")
            agregar_fila(csv, CABECERA, fila)
            print(f"{nombre:<28} {variante:<14} n={n:<8} prom={prom:14.3f} ns/búsqueda  desv={desv:12.3f}",
                  flush=True)


if __name__ == "__main__":
    main()
