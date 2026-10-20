"""
Genera las 9 gráficas pedidas en el taller a partir de los CSV de resultados.

  Punto 1: g1, g2  crecimiento (líneas, log-log) por lenguaje, entrada aleatoria
           g3-g5   efecto del orden de entrada (barras) n = 1.000, 10.000, 100.000, Java
           g6      compilado vs interpretado (barras) n = 1.000.000, entrada aleatoria
  Punto 2: g7, g8  crecimiento del tiempo por búsqueda (líneas, log-log) por lenguaje
           g9      compilado vs interpretado (barras) n = 1.000.000

Convenciones: eje de tiempo SIEMPRE logarítmico; valores estimados con línea punteada y
marcador hueco (líneas) o barra rayada (barras); en las barras el valor va encima de cada barra.
Uso: python3 analisis/graficas.py
"""
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, LogLocator, NullFormatter  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, "resultados")
GRA = os.path.join(RAIZ, "graficas")

ALG_ORD = ["Insertion Sort", "Dual-Pivot QuickSort", "Merge Sort", "Heap Sort", "Radix Sort", "Bucket Sort"]
ALG_BUS = ["Búsqueda Lineal", "Búsqueda Binaria", "Búsqueda Ternaria", "Búsqueda por Saltos",
           "Búsqueda por Interpolación", "Búsqueda Exponencial"]
CORTO_BUS = {"Búsqueda Lineal": "Lineal", "Búsqueda Binaria": "Binaria", "Búsqueda Ternaria": "Ternaria",
             "Búsqueda por Saltos": "Saltos", "Búsqueda por Interpolación": "Interpolación",
             "Búsqueda Exponencial": "Exponencial"}
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]

# Paleta categórica validada (orden fijo) y tinta del gráfico
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
MARCAS = ["o", "s", "^", "D", "v", "P"]
TINTA, TINTA2, TENUE, REJILLA, EJE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": EJE, "axes.labelcolor": TINTA2,
    "xtick.color": TINTA2, "ytick.color": TINTA2, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.titlecolor": TINTA, "legend.frameon": False, "savefig.dpi": 200, "figure.dpi": 100,
})


# ---------------------------------------------------------------- utilidades
def es(x, dec):
    """Número con formato colombiano: punto de miles y coma decimal."""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_ms(ms):
    """Tiempo en ms -> texto corto con la unidad adecuada (3 cifras significativas)."""
    def sig(v):
        if v >= 100:
            return es(v, 0)
        if v >= 10:
            return es(v, 1)
        return es(v, 2)
    if ms < 1e-3:
        return f"{sig(ms * 1e6)} ns"
    if ms < 1:
        return f"{sig(ms * 1e3)} µs"
    if ms < 1000:
        return f"{sig(ms)} ms"
    if ms < 60_000:
        return f"{sig(ms / 1e3)} s"
    if ms < 3_600_000:
        return f"{sig(ms / 6e4)} min"
    return f"{sig(ms / 3.6e6)} h"


def fmt_tick(ms):
    """Etiqueta de marca del eje (potencias de 10): ns, µs, ms o s, sin decimales."""
    for limite, factor, unidad in ((1e-3, 1e6, "ns"), (1, 1e3, "µs"), (1000, 1, "ms")):
        if ms < limite * 0.999:
            return f"{es(ms * factor, 0)} {unidad}"
    return f"{es(ms / 1000, 0)} s"


def eje_tiempo(ax, eje="y"):
    loc = LogLocator(base=10, numticks=30)
    fmt = FuncFormatter(lambda v, _: fmt_tick(v))
    if eje == "y":
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(loc)
        ax.yaxis.set_major_formatter(fmt)
        ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, axis="y", which="major", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)


def eje_n(ax):
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(TAMANOS))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: es(v, 0)))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(700, 1_450_000)
    ax.set_xlabel("n (tamaño del arreglo, escala logarítmica)")


def leer(nombre, unidad_a_ms=1.0):
    """Devuelve dict[(alg, lenguaje, variante, n)] = (tiempo_ms, tipo, desviacion_ms)."""
    ruta = os.path.join(RES, nombre)
    d = {}
    if not os.path.exists(ruta):
        return d
    col_p = "promedio_ms" if "ordenamiento" in nombre else "promedio_ns"
    col_d = "desviacion_ms" if "ordenamiento" in nombre else "desviacion_ns"
    with open(ruta, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            desv = float(r[col_d]) * unidad_a_ms if r[col_d] else None
            d[(r["algoritmo"], r["lenguaje"], r["variante"], int(r["n"]))] = (
                float(r[col_p]) * unidad_a_ms, r["tipo"], desv)
    return d


def guardar(fig, nombre):
    os.makedirs(GRA, exist_ok=True)
    fig.savefig(os.path.join(GRA, nombre), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", nombre)


# ---------------------------------------------------------------- gráficas de líneas
def grafica_crecimiento(datos, algoritmos, lenguaje, variante, titulo, ylabel, archivo, etiquetas=None):
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for i, alg in enumerate(algoritmos):
        pts = [(n, *datos[(alg, lenguaje, variante, n)][:2]) for n in TAMANOS
               if (alg, lenguaje, variante, n) in datos]
        if not pts:
            continue
        color, marca = SERIES[i], MARCAS[i]
        med = [(n, t) for n, t, tipo in pts if tipo == "medido"]
        est = [(n, t) for n, t, tipo in pts if tipo == "estimado"]
        if med:
            ax.plot([p[0] for p in med], [p[1] for p in med], color=color, lw=2, marker=marca, ms=6,
                    markeredgecolor="white", markeredgewidth=1.0, zorder=3)
        if est:
            enlace = ([med[-1]] if med else []) + est
            ax.plot([p[0] for p in enlace], [p[1] for p in enlace], color=color, lw=1.8, ls=(0, (4, 3)), zorder=2)
            ax.plot([p[0] for p in est], [p[1] for p in est], ls="none", marker=marca, ms=6.5,
                    markerfacecolor="white", markeredgecolor=color, markeredgewidth=1.6, zorder=3)
    eje_n(ax)
    eje_tiempo(ax)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo, loc="left")
    nombres = etiquetas or {}
    h = [Line2D([], [], color=SERIES[i], lw=2, marker=MARCAS[i], ms=6, label=nombres.get(a, a))
         for i, a in enumerate(algoritmos)]
    hay_est = any(datos[(a, lenguaje, variante, n)][1] == "estimado" for a in algoritmos for n in TAMANOS
                  if (a, lenguaje, variante, n) in datos)
    if hay_est:
        h += [Line2D([], [], color=TENUE, lw=2, marker="o", ms=5, label="medido"),
              Line2D([], [], color=TENUE, lw=1.8, ls=(0, (4, 3)), marker="o", ms=5.5, markerfacecolor="white",
                     markeredgecolor=TENUE, label="estimado")]
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8.5, labelcolor=TINTA)
    guardar(fig, archivo)


# ---------------------------------------------------------------- gráficas de barras
def grafica_barras(grupos, series, valores, titulo, ylabel, archivo, etiquetas_grupo=None):
    """valores[(grupo, serie)] = (tiempo_ms, tipo). Una barra por serie dentro de cada grupo."""
    k = len(series)
    ancho = 0.8 / k
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    vals = [v[0] for v in valores.values() if v]
    vmin, vmax = min(vals), max(vals)
    piso = vmin / 4
    for j, (serie, color) in enumerate(series):
        for g, grupo in enumerate(grupos):
            v = valores.get((grupo, serie))
            if not v:
                continue
            t, tipo = v
            x = g - 0.4 + ancho * (j + 0.5)
            estimado = tipo == "estimado"
            ax.bar(x, t - piso, bottom=piso, width=ancho * 0.92, color=color if not estimado else "white",
                   edgecolor=color, linewidth=1.2 if estimado else 0, hatch="////" if estimado else None, zorder=2)
            texto = fmt_ms(t) + (" (est.)" if estimado else "")
            ax.text(x, t * 1.12, texto, rotation=90, ha="center", va="bottom", fontsize=7, color=TINTA, zorder=4)
    ax.set_xticks(range(len(grupos)))
    ax.set_xticklabels([(etiquetas_grupo or {}).get(g, g) for g in grupos], fontsize=8.5, color=TINTA)
    ax.set_xlim(-0.6, len(grupos) - 0.4)
    eje_tiempo(ax)
    ax.set_ylim(piso, 10 ** math.ceil(math.log10(vmax * 12)))
    ax.set_ylabel(ylabel)
    ax.set_title(titulo, loc="left")
    h = [Patch(facecolor=c, label=s) for s, c in series]
    if any(v and v[1] == "estimado" for v in valores.values()):
        h.append(Patch(facecolor="white", edgecolor=TENUE, hatch="////", label="estimado"))
    ax.legend(handles=h, loc="lower left", ncol=len(h), fontsize=8.5, labelcolor=TINTA,
              bbox_to_anchor=(0, 1.0), handlelength=1.4, columnspacing=1.2, borderaxespad=0.2)
    ax.set_title(titulo, loc="left", pad=24)
    guardar(fig, archivo)


def main():
    o_java = leer("ordenamiento_java.csv")
    o_py = leer("ordenamiento_python.csv")
    ordn = {**o_java, **o_py}
    b = {**leer("busqueda_java.csv", 1e-6), **leer("busqueda_python.csv", 1e-6)}   # ns -> ms

    print("Punto 1")
    grafica_crecimiento(ordn, ALG_ORD, "Java", "aleatorio",
                        "Crecimiento del tiempo de ordenamiento - Java (entrada aleatoria)",
                        "Tiempo promedio (escala logarítmica)", "g1_crecimiento_ordenamiento_java.png")
    grafica_crecimiento(ordn, ALG_ORD, "Python", "aleatorio",
                        "Crecimiento del tiempo de ordenamiento - Python (entrada aleatoria)",
                        "Tiempo promedio (escala logarítmica)", "g2_crecimiento_ordenamiento_python.png")
    variantes = [("aleatorio", SERIES[0]), ("ascendente", SERIES[1]), ("descendente", SERIES[2])]
    corto = {"Dual-Pivot QuickSort": "Dual-Pivot\nQuickSort", "Insertion Sort": "Insertion\nSort",
             "Merge Sort": "Merge\nSort", "Heap Sort": "Heap\nSort", "Radix Sort": "Radix\nSort",
             "Bucket Sort": "Bucket\nSort"}
    for idx, n in enumerate([1_000, 10_000, 100_000], start=3):
        vals = {(a, v): ordn[(a, "Java", v, n)][:2] for a in ALG_ORD for v, _ in variantes
                if (a, "Java", v, n) in ordn}
        if vals:
            grafica_barras(ALG_ORD, variantes, vals,
                           f"Efecto del orden de entrada - Java, n = {es(n, 0)}",
                           "Tiempo promedio (escala logarítmica)", f"g{idx}_orden_entrada_java_n{n}.png", corto)
    leng = [("Java", SERIES[0]), ("Python", SERIES[1])]
    vals = {(a, l): ordn[(a, l, "aleatorio", 1_000_000)][:2] for a in ALG_ORD for l, _ in leng
            if (a, l, "aleatorio", 1_000_000) in ordn}
    if vals:
        grafica_barras(ALG_ORD, leng, vals, "Compilado (Java) vs interpretado (Python) - n = 1.000.000",
                       "Tiempo promedio (escala logarítmica)",
                       "g6_compilado_vs_interpretado_ordenamiento_n1000000.png", corto)

    print("Punto 2")
    grafica_crecimiento(b, ALG_BUS, "Java", "claves_mixtas",
                        "Crecimiento del tiempo por búsqueda - Java",
                        "Tiempo promedio por búsqueda (escala log.)", "g7_crecimiento_busqueda_java.png", CORTO_BUS)
    grafica_crecimiento(b, ALG_BUS, "Python", "claves_mixtas",
                        "Crecimiento del tiempo por búsqueda - Python",
                        "Tiempo promedio por búsqueda (escala log.)", "g8_crecimiento_busqueda_python.png", CORTO_BUS)
    vals = {(a, l): b[(a, l, "claves_mixtas", 1_000_000)][:2] for a in ALG_BUS for l, _ in leng
            if (a, l, "claves_mixtas", 1_000_000) in b}
    if vals:
        grafica_barras(ALG_BUS, leng, vals, "Compilado (Java) vs interpretado (Python) - búsqueda, n = 1.000.000",
                       "Tiempo promedio por búsqueda (escala log.)",
                       "g9_compilado_vs_interpretado_busqueda_n1000000.png", CORTO_BUS)


if __name__ == "__main__":
    main()
