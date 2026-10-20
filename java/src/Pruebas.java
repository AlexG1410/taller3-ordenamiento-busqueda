import java.util.Arrays;
import java.util.Random;

/** Pruebas de corrección rápidas (arreglos pequeños, con repetidos y casos borde). */
public class Pruebas {
    public static void main(String[] args) {
        Random rnd = new Random(7);
        int casos = 0;
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(300);
            int[] base = new int[n];
            int rango = (t % 3 == 0) ? 20 : 90_000_000;          // con muchos repetidos o no
            for (int i = 0; i < n; i++) base[i] = 10_000_000 + rnd.nextInt(rango);
            if (t % 7 == 0) Arrays.sort(base);                   // ascendente
            if (t % 11 == 0) { Arrays.sort(base); for (int i = 0; i < n / 2; i++) { int x = base[i]; base[i] = base[n-1-i]; base[n-1-i] = x; } }
            int[] ref = base.clone(); Arrays.sort(ref);
            int[][] r = {base.clone(), base.clone(), base.clone(), base.clone(), base.clone(), base.clone()};
            Ordenamiento.insertionSort(r[0]); Ordenamiento.dualPivotQuickSort(r[1]); Ordenamiento.mergeSort(r[2]);
            Ordenamiento.heapSort(r[3]); Ordenamiento.radixSort(r[4]); Ordenamiento.bucketSort(r[5]);
            for (int[] a : r) if (!Arrays.equals(a, ref)) throw new AssertionError("ordenamiento t=" + t);
            // búsquedas: todas las presentes y algunas ausentes
            for (int i = 0; i < n; i++) comprobar(ref, ref[i], true);
            for (int i = 0; i < 50; i++) { int x = 9_000_000 + rnd.nextInt(92_000_000); comprobar(ref, x, Arrays.binarySearch(ref, x) >= 0); }
            casos++;
        }
        System.out.println("OK: " + casos + " casos aleatorios (6 ordenamientos + 6 búsquedas)");
    }
    static void comprobar(int[] a, int x, boolean esta) {
        int[] res = {Busqueda.linearSearch(a, x), Busqueda.binarySearch(a, x), Busqueda.ternarySearch(a, x),
                Busqueda.jumpSearch(a, x), Busqueda.interpolationSearch(a, x), Busqueda.exponentialSearch(a, x)};
        for (int k = 0; k < res.length; k++) {
            boolean ok = esta ? (res[k] >= 0 && a[res[k]] == x) : res[k] == -1;
            if (!ok) throw new AssertionError("búsqueda " + k + " x=" + x + " res=" + res[k]);
        }
    }
}
