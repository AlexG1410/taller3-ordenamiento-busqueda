"""Pruebas de corrección rápidas (listas pequeñas, con repetidos y casos borde)."""
import bisect
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import busqueda as bq  # noqa: E402
import ordenamiento as o  # noqa: E402

ORD = [o.insertion_sort, o.dual_pivot_quick_sort, o.merge_sort, o.heap_sort, o.radix_sort, o.bucket_sort]
BUS = [bq.linear_search, bq.binary_search, bq.ternary_search, bq.jump_search,
       bq.interpolation_search, bq.exponential_search]


def comprobar(a, x, esta):
    for f in BUS:
        r = f(a, x)
        ok = (r >= 0 and a[r] == x) if esta else r == -1
        assert ok, (f.__name__, x, r)


rnd = random.Random(7)
casos = 0
for t in range(2000):
    n = 1 + rnd.randrange(300)
    rango = 20 if t % 3 == 0 else 90_000_000
    base = [10_000_000 + rnd.randrange(rango) for _ in range(n)]
    if t % 7 == 0:
        base.sort()
    if t % 11 == 0:
        base.sort(reverse=True)
    ref = sorted(base)
    for f in ORD:
        c = base[:]
        f(c)
        assert c == ref, (f.__name__, t)
    for x in ref:
        comprobar(ref, x, True)
    for _ in range(50):
        x = 9_000_000 + rnd.randrange(92_000_000)
        i = bisect.bisect_left(ref, x)
        comprobar(ref, x, i < n and ref[i] == x)
    casos += 1
print(f"OK: {casos} casos aleatorios (6 ordenamientos + 6 búsquedas)")
