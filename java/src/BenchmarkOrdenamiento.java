import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Locale;
import java.util.function.Consumer;

/**
 * Medición de los algoritmos de ordenamiento (Punto 1) en Java (lenguaje compilado).
 *
 * Uso: java -cp java/out BenchmarkOrdenamiento <algoritmo> <carpetaDatos> <archivoCsv>
 *      algoritmo: insertion | dualpivot | merge | heap | radix | bucket
 *
 * Protocolo (condiciones generales del taller):
 *  - Los datos se leen de los archivos ANTES de medir; la lectura no se mide.
 *  - Una ejecución de calentamiento (JIT) que NO entra en el promedio.
 *  - 5 repeticiones, cada una sobre una copia nueva del arreglo original (la copia no se mide).
 *  - Tiempo con System.nanoTime(), solo alrededor de la llamada al algoritmo.
 *  - Después de cada ejecución, fuera del tiempo medido, se verifica que el resultado sea
 *    idéntico al arreglo ascendente de referencia (mismo orden y mismos elementos).
 *  - Regla de 5 minutos: antes de ejecutar un tamaño se predice su tiempo con la complejidad
 *    teórica y la medición del tamaño anterior; si supera 5 minutos no se ejecuta y se estima.
 *  - Si el algoritmo falla (p. ej. StackOverflowError) el error se registra y el tiempo se estima.
 */
public class BenchmarkOrdenamiento {

    static final int[] TAMANOS = {1_000, 10_000, 100_000, 1_000_000};
    static final String[] VARIANTES = {"aleatorio", "ascendente", "descendente"};
    static final int REPETICIONES = 5;
    static final double LIMITE_MS = 5 * 60 * 1000.0;
    static final String CABECERA = "algoritmo,lenguaje,variante,n,rep1_ms,rep2_ms,rep3_ms,rep4_ms,rep5_ms,"
            + "promedio_ms,desviacion_ms,tipo,observacion";

    /** Función de crecimiento teórica del caso que corresponde a cada variante de entrada. */
    static double complejidad(String alg, String variante, int n) {
        double lg = Math.log(n) / Math.log(2);
        switch (alg) {
            case "insertion":
                return variante.equals("ascendente") ? n : (double) n * n;
            case "dualpivot":
                return variante.equals("aleatorio") ? n * lg : (double) n * n;
            case "merge":
            case "heap":
                return n * lg;
            default: // radix (d = 8 fijo) y bucket (distribución uniforme)
                return n;
        }
    }

    static String nombreModelo(String alg, String variante) {
        double a = complejidad(alg, variante, 1000), b = complejidad(alg, variante, 10000);
        double r = b / a;
        if (r > 50) {
            return "O(n^2)";
        }
        if (r > 11) {
            return "O(n log n)";
        }
        return "O(n)";
    }

    public static void main(String[] args) throws IOException {
        String clave = args[0];
        Path datos = Paths.get(args[1]);
        Path csv = Paths.get(args[2]);

        String nombre;
        Consumer<int[]> algoritmo;
        switch (clave) {
            case "insertion": nombre = "Insertion Sort"; algoritmo = Ordenamiento::insertionSort; break;
            case "dualpivot": nombre = "Dual-Pivot QuickSort"; algoritmo = Ordenamiento::dualPivotQuickSort; break;
            case "merge": nombre = "Merge Sort"; algoritmo = Ordenamiento::mergeSort; break;
            case "heap": nombre = "Heap Sort"; algoritmo = Ordenamiento::heapSort; break;
            case "radix": nombre = "Radix Sort"; algoritmo = Ordenamiento::radixSort; break;
            case "bucket": nombre = "Bucket Sort"; algoritmo = Ordenamiento::bucketSort; break;
            default: throw new IllegalArgumentException("Algoritmo desconocido: " + clave);
        }

        for (String variante : VARIANTES) {
            int nRef = -1;
            double tRef = -1;
            for (int n : TAMANOS) {
                int[] original = Utilidades.leerEnteros(datos.resolve("n_" + n + "_" + variante + ".txt"));
                int[] referencia = Utilidades.leerEnteros(datos.resolve("n_" + n + "_ascendente.txt"));
                String modelo = nombreModelo(clave, variante);
                double factor = nRef > 0 ? complejidad(clave, variante, n) / complejidad(clave, variante, nRef) : -1;
                double previsto = nRef > 0 ? tRef * factor : -1;
                String base = nRef > 0
                        ? String.format(Locale.ROOT, "%s a partir de n=%d (t=%.3f ms x %.2f)", modelo, nRef, tRef, factor)
                        : "sin tamaño menor medido";

                if (previsto > LIMITE_MS) {
                    String obs = String.format(Locale.ROOT,
                            "No ejecutado: tiempo previsto %.1f s > 5 min. Estimado con %s", previsto / 1000, base);
                    escribirEstimado(csv, nombre, variante, n, previsto, obs);
                    continue;
                }

                try {
                    // Calentamiento (no se incluye en el promedio)
                    int[] copia = original.clone();
                    long t0 = System.nanoTime();
                    algoritmo.accept(copia);
                    long t1 = System.nanoTime();
                    verificar(copia, referencia, nombre, variante, n);
                    double tCal = (t1 - t0) / 1e6;
                    if (tCal > LIMITE_MS) {
                        String obs = String.format(Locale.ROOT,
                                "Ejecución de calentamiento tardó %.1f s > 5 min; no se repitió. Estimado con %s",
                                tCal / 1000, base);
                        escribirEstimado(csv, nombre, variante, n, previsto > 0 ? previsto : tCal, obs);
                        continue;
                    }

                    double[] reps = new double[REPETICIONES];
                    for (int r = 0; r < REPETICIONES; r++) {
                        int[] c = original.clone();          // copia nueva, fuera del tiempo medido
                        long a = System.nanoTime();
                        algoritmo.accept(c);
                        long b = System.nanoTime();
                        verificar(c, referencia, nombre, variante, n);   // fuera del tiempo medido
                        reps[r] = (b - a) / 1e6;
                    }
                    double prom = Utilidades.promedio(reps);
                    double desv = Utilidades.desviacion(reps);
                    StringBuilder fila = new StringBuilder();
                    fila.append(nombre).append(",Java,").append(variante).append(',').append(n);
                    for (double t : reps) {
                        fila.append(',').append(Utilidades.num(t));
                    }
                    fila.append(',').append(Utilidades.num(prom)).append(',').append(Utilidades.num(desv));
                    fila.append(",medido,").append(Utilidades.texto(
                            String.format(Locale.ROOT, "Calentamiento excluido: %.3f ms. Verificado OK", tCal)));
                    Utilidades.agregarFila(csv, CABECERA, fila.toString());
                    System.out.printf(Locale.ROOT, "%-22s %-12s n=%-8d prom=%12.3f ms  desv=%10.3f ms%n",
                            nombre, variante, n, prom, desv);
                    nRef = n;
                    tRef = prom;
                } catch (StackOverflowError e) {
                    String obs = String.format(Locale.ROOT,
                            "Falla: java.lang.StackOverflowError (desbordamiento de la pila de llamadas, -Xss por "
                            + "defecto = 1 MB) durante la ejecución. Estimado con %s", base);
                    escribirEstimado(csv, nombre, variante, n, previsto, obs);
                }
            }
        }
    }

    static void verificar(int[] resultado, int[] referencia, String nombre, String variante, int n) {
        if (!Arrays.equals(resultado, referencia)) {
            throw new IllegalStateException("Resultado incorrecto: " + nombre + " " + variante + " n=" + n);
        }
    }

    static void escribirEstimado(Path csv, String nombre, String variante, int n, double estimado, String obs)
            throws IOException {
        String fila = nombre + ",Java," + variante + "," + n + ",,,,,," + Utilidades.num(estimado)
                + ",,estimado," + Utilidades.texto(obs);
        Utilidades.agregarFila(csv, CABECERA, fila);
        System.out.printf(Locale.ROOT, "%-22s %-12s n=%-8d ESTIMADO=%12.3f ms  (%s)%n",
                nombre, variante, n, estimado, obs);
    }
}
