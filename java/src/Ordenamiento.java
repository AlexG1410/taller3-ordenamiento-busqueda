import java.util.ArrayList;

/**
 * Algoritmos de ordenamiento - Taller de Ordenamiento y Búsqueda.
 *
 * Todas las implementaciones siguen el código de GeeksforGeeks (fuentes en cada método)
 * y son la MISMA implementación que la versión en Python (python/ordenamiento.py).
 * Todas ordenan de forma ascendente y modifican el arreglo recibido.
 */
public final class Ordenamiento {

    private Ordenamiento() { }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // ------------------------------------------------------------------
    // 1. Insertion Sort
    // Fuente: https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
    // ------------------------------------------------------------------
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; ++i) {
            int key = arr[i];
            int j = i - 1;
            // Desplaza a la derecha los elementos mayores que key
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }
            arr[j + 1] = key;
        }
    }

    // ------------------------------------------------------------------
    // 2. Dual-Pivot QuickSort (pivotes: primer y último elemento)
    // Fuente: https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/
    // ------------------------------------------------------------------
    public static void dualPivotQuickSort(int[] arr) {
        dualPivotQuickSort(arr, 0, arr.length - 1);
    }

    private static void dualPivotQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            int[] piv = partition(arr, low, high);
            dualPivotQuickSort(arr, low, piv[0] - 1);        // menores que p
            dualPivotQuickSort(arr, piv[0] + 1, piv[1] - 1); // entre p y q
            dualPivotQuickSort(arr, piv[1] + 1, high);       // mayores que q
        }
    }

    private static int[] partition(int[] arr, int low, int high) {
        if (arr[low] > arr[high]) {
            swap(arr, low, high);
        }
        int j = low + 1;                 // frontera de los menores que p
        int g = high - 1, k = low + 1;   // g: frontera de los mayores que q; k: elemento actual
        int p = arr[low], q = arr[high]; // p = pivote izquierdo, q = pivote derecho
        while (k <= g) {
            if (arr[k] < p) {
                swap(arr, k, j);
                j++;
            } else if (arr[k] >= q) {
                while (arr[g] > q && k < g) {
                    g--;
                }
                swap(arr, k, g);
                g--;
                if (arr[k] < p) {
                    swap(arr, k, j);
                    j++;
                }
            }
            k++;
        }
        j--;
        g++;
        swap(arr, low, j);   // p a su posición final
        swap(arr, high, g);  // q a su posición final
        return new int[] {j, g};
    }

    // ------------------------------------------------------------------
    // 3. Merge Sort
    // Fuente: https://www.geeksforgeeks.org/dsa/merge-sort/
    // ------------------------------------------------------------------
    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    private static void merge(int[] arr, int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;
        int[] left = new int[n1];
        int[] right = new int[n2];
        for (int i = 0; i < n1; ++i) {
            left[i] = arr[l + i];
        }
        for (int j = 0; j < n2; ++j) {
            right[j] = arr[m + 1 + j];
        }
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (left[i] <= right[j]) {   // <= conserva la estabilidad
                arr[k] = left[i];
                i++;
            } else {
                arr[k] = right[j];
                j++;
            }
            k++;
        }
        while (i < n1) {
            arr[k] = left[i];
            i++;
            k++;
        }
        while (j < n2) {
            arr[k] = right[j];
            j++;
            k++;
        }
    }

    // ------------------------------------------------------------------
    // 4. Heap Sort
    // Fuente: https://www.geeksforgeeks.org/dsa/heap-sort/
    // ------------------------------------------------------------------
    public static void heapSort(int[] arr) {
        int n = arr.length;
        // Construir el max-heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        // Extraer uno a uno el máximo
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    private static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int l = 2 * i + 1;
        int r = 2 * i + 2;
        if (l < n && arr[l] > arr[largest]) {
            largest = l;
        }
        if (r < n && arr[r] > arr[largest]) {
            largest = r;
        }
        if (largest != i) {
            swap(arr, i, largest);
            heapify(arr, n, largest);
        }
    }

    // ------------------------------------------------------------------
    // 5. Radix Sort (LSD, base 10, Counting Sort estable por dígito)
    // Fuente: https://www.geeksforgeeks.org/dsa/radix-sort/
    // ------------------------------------------------------------------
    public static void radixSort(int[] arr) {
        int n = arr.length;
        int m = getMax(arr, n);
        // Una pasada de counting sort por cada dígito (8 pasadas para números de 8 dígitos)
        for (int exp = 1; m / exp > 0; exp *= 10) {
            countSort(arr, n, exp);
        }
    }

    private static int getMax(int[] arr, int n) {
        int mx = arr[0];
        for (int i = 1; i < n; i++) {
            if (arr[i] > mx) {
                mx = arr[i];
            }
        }
        return mx;
    }

    private static void countSort(int[] arr, int n, int exp) {
        int[] output = new int[n];
        int[] count = new int[10];
        for (int i = 0; i < n; i++) {
            count[(arr[i] / exp) % 10]++;
        }
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        for (int i = n - 1; i >= 0; i--) {   // de derecha a izquierda: estable
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }
        for (int i = 0; i < n; i++) {
            arr[i] = output[i];
        }
    }

    // ------------------------------------------------------------------
    // 6. Bucket Sort
    // Fuente: https://www.geeksforgeeks.org/dsa/bucket-sort-2/
    // El original de GfG ordena reales en [0, 1) con n cubetas e índice n*x.
    // Adaptación a enteros: x se normaliza a [0, 1) con (v - min) / (max - min + 1),
    // por lo que la cubeta de v es  floor( (v - min) * k / (max - min + 1) ),  con k = n cubetas.
    // Cada cubeta se ordena con Insertion Sort, igual que en GfG.
    // ------------------------------------------------------------------
    @SuppressWarnings({"unchecked", "rawtypes"})
    public static void bucketSort(int[] arr) {
        int n = arr.length;
        if (n <= 0) {
            return;
        }
        int min = arr[0], max = arr[0];
        for (int i = 1; i < n; i++) {
            if (arr[i] < min) {
                min = arr[i];
            }
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        int k = n;                               // número de cubetas
        long rango = (long) max - min + 1;
        ArrayList<Integer>[] buckets = new ArrayList[k];
        for (int i = 0; i < k; i++) {
            buckets[i] = new ArrayList<>();
        }
        for (int i = 0; i < n; i++) {
            int bi = (int) (((long) (arr[i] - min) * k) / rango);
            buckets[bi].add(arr[i]);
        }
        for (int i = 0; i < k; i++) {
            insertionSortBucket(buckets[i]);
        }
        int index = 0;
        for (int i = 0; i < k; i++) {
            ArrayList<Integer> b = buckets[i];
            for (int j = 0, sz = b.size(); j < sz; j++) {
                arr[index++] = b.get(j);
            }
        }
    }

    private static void insertionSortBucket(ArrayList<Integer> bucket) {
        for (int i = 1; i < bucket.size(); i++) {
            int key = bucket.get(i);
            int j = i - 1;
            while (j >= 0 && bucket.get(j) > key) {
                bucket.set(j + 1, bucket.get(j));
                j--;
            }
            bucket.set(j + 1, key);
        }
    }
}
