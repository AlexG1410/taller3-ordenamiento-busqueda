import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Locale;

/**
 * Medición de los algoritmos de búsqueda (Punto 2) en Java (lenguaje compilado).
 *
 * Uso: java -cp java/out BenchmarkBusqueda <algoritmo> <carpetaDatos> <archivoCsv>
 *      algoritmo: lineal | binaria | ternaria | saltos | interpolacion | exponencial
 *
 * - Datos: arreglos ascendentes del Punto 1 (n_<n>_ascendente.txt).
 * - claves_mixtas: las 1.000 claves del archivo claves_n_<n>.txt (500 presentes, 500 ausentes).
 * - pos_inicio / pos_centro / pos_final: 1.000 búsquedas de la clave arr[0], arr[(n-1)/2], arr[n-1].
 * - Se mide el tiempo TOTAL del lote de 1.000 búsquedas y se reporta el promedio por búsqueda
 *   (total / 1.000). 1 calentamiento + 5 repeticiones. La corrección se verifica fuera del tiempo.
 */
public class BenchmarkBusqueda {

    interface Buscador {
        int buscar(int[] arr, int x);
    }

    static final int[] TAMANOS = {1_000, 10_000, 100_000, 1_000_000};
    static final int REPETICIONES = 5;
    static final int BUSQUEDAS = 1_000;
    static final String CABECERA = "algoritmo,lenguaje,variante,n,rep1_ns,rep2_ns,rep3_ns,rep4_ns,rep5_ns,"
            + "promedio_ns,desviacion_ns,tipo,observacion";

    /** Evita que el compilador JIT elimine las búsquedas por considerar inútil su resultado. */
    static volatile long sumidero;

    public static void main(String[] args) throws IOException {
        String clave = args[0];
        Path datos = Paths.get(args[1]);
        Path csv = Paths.get(args[2]);

        String nombre;
        Buscador alg;
        switch (clave) {
            case "lineal": nombre = "Búsqueda Lineal"; alg = Busqueda::linearSearch; break;
            case "binaria": nombre = "Búsqueda Binaria"; alg = Busqueda::binarySearch; break;
            case "ternaria": nombre = "Búsqueda Ternaria"; alg = Busqueda::ternarySearch; break;
            case "saltos": nombre = "Búsqueda por Saltos"; alg = Busqueda::jumpSearch; break;
            case "interpolacion": nombre = "Búsqueda por Interpolación"; alg = Busqueda::interpolationSearch; break;
            case "exponencial": nombre = "Búsqueda Exponencial"; alg = Busqueda::exponentialSearch; break;
            default: throw new IllegalArgumentException("Algoritmo desconocido: " + clave);
        }

        for (int n : TAMANOS) {
            int[] arr = Utilidades.leerEnteros(datos.resolve("n_" + n + "_ascendente.txt"));
            int[] claves = Utilidades.leerEnteros(datos.resolve("claves_n_" + n + ".txt"));
            HashSet<Integer> conjunto = new HashSet<>();
            for (int v : arr) {
                conjunto.add(v);
            }

            String[] variantes = {"claves_mixtas", "pos_inicio", "pos_centro", "pos_final"};
            for (String variante : variantes) {
                int[] lote;
                switch (variante) {
                    case "claves_mixtas": lote = claves; break;
                    case "pos_inicio": lote = new int[BUSQUEDAS]; Arrays.fill(lote, arr[0]); break;
                    case "pos_centro": lote = new int[BUSQUEDAS]; Arrays.fill(lote, arr[(n - 1) / 2]); break;
                    default: lote = new int[BUSQUEDAS]; Arrays.fill(lote, arr[n - 1]); break;
                }

                // Verificación de corrección (fuera del tiempo medido)
                for (int x : lote) {
                    int idx = alg.buscar(arr, x);
                    boolean ok = conjunto.contains(x) ? (idx >= 0 && arr[idx] == x) : idx == -1;
                    if (!ok) {
                        throw new IllegalStateException("Resultado incorrecto: " + nombre + " n=" + n + " x=" + x);
                    }
                }

                // Calentamiento (no se incluye)
                long s = 0;
                for (int x : lote) {
                    s += alg.buscar(arr, x);
                }
                sumidero += s;

                double[] reps = new double[REPETICIONES];
                for (int r = 0; r < REPETICIONES; r++) {
                    long acumulado = 0;
                    long a = System.nanoTime();
                    for (int x : lote) {
                        acumulado += alg.buscar(arr, x);
                    }
                    long b = System.nanoTime();
                    sumidero += acumulado;
                    reps[r] = (b - a) / (double) BUSQUEDAS;   // ns promedio por búsqueda
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
                        "Tiempo por búsqueda = tiempo total de 1000 búsquedas / 1000. Verificado OK"));
                Utilidades.agregarFila(csv, CABECERA, fila.toString());
                System.out.printf(Locale.ROOT, "%-28s %-14s n=%-8d prom=%14.3f ns/búsqueda  desv=%12.3f%n",
                        nombre, variante, n, prom, desv);
            }
        }
    }
}
