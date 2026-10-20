"""
Algoritmos de búsqueda - Taller de Ordenamiento y Búsqueda.

Misma implementación que java/src/Busqueda.java, basada en GeeksforGeeks
(fuente en cada función). Devuelven el índice de x en la lista ordenada
ascendentemente, o -1 si x no está.
"""
import math


# Búsqueda Lineal (referencia)
# Fuente: https://www.geeksforgeeks.org/dsa/linear-search/
def linear_search(arr, x):
    n = len(arr)
    for i in range(n):
        if arr[i] == x:
            return i
    return -1


# Búsqueda Binaria (iterativa)
# Fuente: https://www.geeksforgeeks.org/dsa/binary-search/
def binary_search(arr, x):
    return _binary_search(arr, 0, len(arr) - 1, x)


def _binary_search(arr, low, high, x):
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# Búsqueda Ternaria (iterativa)
# Fuente: https://www.geeksforgeeks.org/dsa/ternary-search/
def ternary_search(arr, key):
    l = 0
    r = len(arr) - 1
    while r >= l:
        mid1 = l + (r - l) // 3
        mid2 = r - (r - l) // 3
        if arr[mid1] == key:
            return mid1
        if arr[mid2] == key:
            return mid2
        if key < arr[mid1]:
            r = mid1 - 1
        elif key > arr[mid2]:
            l = mid2 + 1
        else:
            l = mid1 + 1
            r = mid2 - 1
    return -1


# Búsqueda por Saltos (Jump Search), salto = floor(sqrt(n))
# Fuente: https://www.geeksforgeeks.org/dsa/jump-search/
def jump_search(arr, x):
    n = len(arr)
    salto = int(math.floor(math.sqrt(n)))
    step = salto
    prev = 0
    # Saltar por bloques hasta encontrar el bloque donde podría estar x
    while arr[min(step, n) - 1] < x:
        prev = step
        step += salto
        if prev >= n:
            return -1
    # Búsqueda lineal dentro del bloque
    while arr[prev] < x:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[prev] == x:
        return prev
    return -1


# Búsqueda por Interpolación (iterativa)
# Fuente: https://www.geeksforgeeks.org/dsa/interpolation-search/
# pos = lo + (x - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo]); se multiplica antes de dividir
# y se protege la división entre cero cuando arr[hi] == arr[lo].
def interpolation_search(arr, x):
    lo = 0
    hi = len(arr) - 1
    while lo <= hi and arr[lo] <= x <= arr[hi]:
        if arr[hi] == arr[lo]:          # incluye lo == hi
            return lo if arr[lo] == x else -1
        pos = lo + (x - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])
        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


# Búsqueda Exponencial: duplica i hasta pasar x y luego búsqueda binaria en [i/2, min(i, n-1)]
# Fuente: https://www.geeksforgeeks.org/dsa/exponential-search/
def exponential_search(arr, x):
    n = len(arr)
    if arr[0] == x:
        return 0
    i = 1
    while i < n and arr[i] <= x:
        i = i * 2
    return _binary_search(arr, i // 2, min(i, n - 1), x)
