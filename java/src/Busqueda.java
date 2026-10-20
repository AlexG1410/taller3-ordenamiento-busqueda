/**
 * Algoritmos de búsqueda - Taller de Ordenamiento y Búsqueda.
 *
 * Implementaciones basadas en GeeksforGeeks (fuentes en cada método) e idénticas
 * a la versión en Python (python/busqueda.py). Todas devuelven el índice de x
 * en el arreglo ordenado ascendentemente, o -1 si x no está.
 */
public final class Busqueda {

    private Busqueda() { }

    // ------------------------------------------------------------------
    // Búsqueda Lineal (referencia)
    // Fuente: https://www.geeksforgeeks.org/dsa/linear-search/
    // ------------------------------------------------------------------
    public static int linearSearch(int[] arr, int x) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            if (arr[i] == x) {
                return i;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda Binaria (iterativa)
    // Fuente: https://www.geeksforgeeks.org/dsa/binary-search/
    // ------------------------------------------------------------------
    public static int binarySearch(int[] arr, int x) {
        return binarySearch(arr, 0, arr.length - 1, x);
    }

    static int binarySearch(int[] arr, int low, int high, int x) {
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == x) {
                return mid;
            }
            if (arr[mid] < x) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda Ternaria (iterativa)
    // Fuente: https://www.geeksforgeeks.org/dsa/ternary-search/
    // ------------------------------------------------------------------
    public static int ternarySearch(int[] arr, int key) {
        int l = 0, r = arr.length - 1;
        while (r >= l) {
            int mid1 = l + (r - l) / 3;
            int mid2 = r - (r - l) / 3;
            if (arr[mid1] == key) {
                return mid1;
            }
            if (arr[mid2] == key) {
                return mid2;
            }
            if (key < arr[mid1]) {
                r = mid1 - 1;
            } else if (key > arr[mid2]) {
                l = mid2 + 1;
            } else {
                l = mid1 + 1;
                r = mid2 - 1;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda por Saltos (Jump Search), salto = floor(sqrt(n))
    // Fuente: https://www.geeksforgeeks.org/dsa/jump-search/
    // ------------------------------------------------------------------
    public static int jumpSearch(int[] arr, int x) {
        int n = arr.length;
        int salto = (int) Math.floor(Math.sqrt(n));
        int step = salto;
        int prev = 0;
        // Saltar por bloques hasta encontrar el bloque donde podría estar x
        while (arr[Math.min(step, n) - 1] < x) {
            prev = step;
            step += salto;
            if (prev >= n) {
                return -1;
            }
        }
        // Búsqueda lineal dentro del bloque
        while (arr[prev] < x) {
            prev++;
            if (prev == Math.min(step, n)) {
                return -1;
            }
        }
        if (arr[prev] == x) {
            return prev;
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda por Interpolación (iterativa)
    // Fuente: https://www.geeksforgeeks.org/dsa/interpolation-search/
    // Fórmula: pos = lo + (x - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo]).
    // Se multiplica antes de dividir (en long) para no perder precisión ni desbordar,
    // y se protege la división entre cero cuando arr[hi] == arr[lo].
    // ------------------------------------------------------------------
    public static int interpolationSearch(int[] arr, int x) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi && x >= arr[lo] && x <= arr[hi]) {
            if (arr[hi] == arr[lo]) {   // incluye lo == hi
                return (arr[lo] == x) ? lo : -1;
            }
            int pos = lo + (int) (((long) (x - arr[lo]) * (hi - lo)) / (arr[hi] - arr[lo]));
            if (arr[pos] == x) {
                return pos;
            }
            if (arr[pos] < x) {
                lo = pos + 1;
            } else {
                hi = pos - 1;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda Exponencial: duplica i hasta pasar x y luego búsqueda binaria en [i/2, min(i, n-1)]
    // Fuente: https://www.geeksforgeeks.org/dsa/exponential-search/
    // ------------------------------------------------------------------
    public static int exponentialSearch(int[] arr, int x) {
        int n = arr.length;
        if (arr[0] == x) {
            return 0;
        }
        int i = 1;
        while (i < n && arr[i] <= x) {
            i = i * 2;
        }
        return binarySearch(arr, i / 2, Math.min(i, n - 1), x);
    }
}
