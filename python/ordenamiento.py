"""
Algoritmos de ordenamiento - Taller de Ordenamiento y Búsqueda.

Misma implementación que java/src/Ordenamiento.java, basada en GeeksforGeeks
(fuente en cada función). Todas ordenan ascendentemente y modifican la lista recibida.
"""


# ----------------------------------------------------------------------
# 1. Insertion Sort
# Fuente: https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
# ----------------------------------------------------------------------
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Desplaza a la derecha los elementos mayores que key
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j = j - 1
        arr[j + 1] = key


# ----------------------------------------------------------------------
# 2. Dual-Pivot QuickSort (pivotes: primer y último elemento)
# Fuente: https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/
# ----------------------------------------------------------------------
def dual_pivot_quick_sort(arr):
    _dual_pivot_quick_sort(arr, 0, len(arr) - 1)


def _dual_pivot_quick_sort(arr, low, high):
    if low < high:
        lp, rp = _partition(arr, low, high)
        _dual_pivot_quick_sort(arr, low, lp - 1)        # menores que p
        _dual_pivot_quick_sort(arr, lp + 1, rp - 1)     # entre p y q
        _dual_pivot_quick_sort(arr, rp + 1, high)       # mayores que q


def _partition(arr, low, high):
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    j = low + 1                     # frontera de los menores que p
    g = high - 1                    # frontera de los mayores que q
    k = low + 1                     # elemento actual
    p = arr[low]                    # pivote izquierdo
    q = arr[high]                   # pivote derecho
    while k <= g:
        if arr[k] < p:
            arr[k], arr[j] = arr[j], arr[k]
            j += 1
        elif arr[k] >= q:
            while arr[g] > q and k < g:
                g -= 1
            arr[k], arr[g] = arr[g], arr[k]
            g -= 1
            if arr[k] < p:
                arr[k], arr[j] = arr[j], arr[k]
                j += 1
        k += 1
    j -= 1
    g += 1
    arr[low], arr[j] = arr[j], arr[low]      # p a su posición final
    arr[high], arr[g] = arr[g], arr[high]    # q a su posición final
    return j, g


# ----------------------------------------------------------------------
# 3. Merge Sort
# Fuente: https://www.geeksforgeeks.org/dsa/merge-sort/
# ----------------------------------------------------------------------
def merge_sort(arr):
    _merge_sort(arr, 0, len(arr) - 1)


def _merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m)
        _merge_sort(arr, m + 1, r)
        _merge(arr, l, m, r)


def _merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    left = [0] * n1
    right = [0] * n2
    for i in range(n1):
        left[i] = arr[l + i]
    for j in range(n2):
        right[j] = arr[m + 1 + j]
    i = 0
    j = 0
    k = l
    while i < n1 and j < n2:
        if left[i] <= right[j]:      # <= conserva la estabilidad
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = left[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = right[j]
        j += 1
        k += 1


# ----------------------------------------------------------------------
# 4. Heap Sort
# Fuente: https://www.geeksforgeeks.org/dsa/heap-sort/
# ----------------------------------------------------------------------
def heap_sort(arr):
    n = len(arr)
    # Construir el max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    # Extraer uno a uno el máximo
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)


def _heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


# ----------------------------------------------------------------------
# 5. Radix Sort (LSD, base 10, Counting Sort estable por dígito)
# Fuente: https://www.geeksforgeeks.org/dsa/radix-sort/
# ----------------------------------------------------------------------
def radix_sort(arr):
    n = len(arr)
    m = _get_max(arr, n)
    exp = 1
    # Una pasada de counting sort por cada dígito (8 pasadas para números de 8 dígitos)
    while m // exp > 0:
        _count_sort(arr, n, exp)
        exp *= 10


def _get_max(arr, n):
    mx = arr[0]
    for i in range(1, n):
        if arr[i] > mx:
            mx = arr[i]
    return mx


def _count_sort(arr, n, exp):
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        count[(arr[i] // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:                     # de derecha a izquierda: estable
        output[count[(arr[i] // exp) % 10] - 1] = arr[i]
        count[(arr[i] // exp) % 10] -= 1
        i -= 1
    for i in range(n):
        arr[i] = output[i]


# ----------------------------------------------------------------------
# 6. Bucket Sort
# Fuente: https://www.geeksforgeeks.org/dsa/bucket-sort-2/
# El original de GfG ordena reales en [0, 1) con n cubetas e índice n*x.
# Adaptación a enteros: x se normaliza a [0, 1) con (v - min) / (max - min + 1),
# por lo que la cubeta de v es  floor( (v - min) * k / (max - min + 1) ),  con k = n cubetas.
# Cada cubeta se ordena con Insertion Sort, igual que en GfG.
# ----------------------------------------------------------------------
def bucket_sort(arr):
    n = len(arr)
    if n <= 0:
        return
    mn = arr[0]
    mx = arr[0]
    for i in range(1, n):
        if arr[i] < mn:
            mn = arr[i]
        if arr[i] > mx:
            mx = arr[i]
    k = n                                  # número de cubetas
    rango = mx - mn + 1
    buckets = [[] for _ in range(k)]
    for i in range(n):
        bi = (arr[i] - mn) * k // rango
        buckets[bi].append(arr[i])
    for i in range(k):
        _insertion_sort_bucket(buckets[i])
    index = 0
    for i in range(k):
        b = buckets[i]
        for j in range(len(b)):
            arr[index] = b[j]
            index += 1


def _insertion_sort_bucket(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
