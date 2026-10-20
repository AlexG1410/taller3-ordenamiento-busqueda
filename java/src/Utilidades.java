import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Locale;

/** Utilidades comunes de los programas de medición (lectura de datos, estadística, CSV). */
public final class Utilidades {

    private Utilidades() { }

    /** Lee un archivo de texto plano con un entero por línea. */
    public static int[] leerEnteros(Path archivo) throws IOException {
        int capacidad = 1024;
        int[] datos = new int[capacidad];
        int n = 0;
        try (BufferedReader br = Files.newBufferedReader(archivo, StandardCharsets.UTF_8)) {
            String linea;
            while ((linea = br.readLine()) != null) {
                linea = linea.trim();
                if (linea.isEmpty()) {
                    continue;
                }
                if (n == capacidad) {
                    capacidad *= 2;
                    int[] nuevo = new int[capacidad];
                    System.arraycopy(datos, 0, nuevo, 0, n);
                    datos = nuevo;
                }
                datos[n++] = Integer.parseInt(linea);
            }
        }
        int[] resultado = new int[n];
        System.arraycopy(datos, 0, resultado, 0, n);
        return resultado;
    }

    public static double promedio(double[] v) {
        double s = 0;
        for (double x : v) {
            s += x;
        }
        return s / v.length;
    }

    /** Desviación estándar muestral (divide entre n - 1). */
    public static double desviacion(double[] v) {
        double m = promedio(v);
        double s = 0;
        for (double x : v) {
            s += (x - m) * (x - m);
        }
        return Math.sqrt(s / (v.length - 1));
    }

    public static String num(double x) {
        return String.format(Locale.ROOT, "%.6f", x);
    }

    /** Agrega una fila al CSV; escribe la cabecera si el archivo no existe. */
    public static void agregarFila(Path csv, String cabecera, String fila) throws IOException {
        boolean nuevo = !Files.exists(csv);
        if (csv.getParent() != null) {
            Files.createDirectories(csv.getParent());
        }
        try (PrintWriter pw = new PrintWriter(Files.newBufferedWriter(csv, StandardCharsets.UTF_8,
                StandardOpenOption.CREATE, StandardOpenOption.APPEND))) {
            if (nuevo) {
                pw.println(cabecera);
            }
            pw.println(fila);
        }
    }

    /** Encierra un texto entre comillas para el CSV. */
    public static String texto(String s) {
        return "\"" + s.replace("\"", "'") + "\"";
    }
}
