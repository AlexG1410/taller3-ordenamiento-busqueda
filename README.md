# Taller 3: algoritmos de ordenamiento y búsqueda

Proyecto de Análisis de Algoritmos de la Universidad del Quindío. Compara seis algoritmos de ordenamiento y seis de búsqueda mediante implementaciones en Java y Python.

**Integrantes:**

- Alex David Gutiérrez Jurado.
- Juan David Mejía Barbosa.
- Kevyn Ramírez González.

## Algoritmos implementados

| Ordenamiento | Identificador |
|---|---|
| Insertion Sort | `insertion` |
| Dual-Pivot QuickSort | `dualpivot` |
| Merge Sort | `merge` |
| Heap Sort | `heap` |
| Radix Sort | `radix` |
| Bucket Sort | `bucket` |

| Búsqueda | Identificador |
|---|---|
| Lineal | `lineal` |
| Binaria | `binaria` |
| Ternaria | `ternaria` |
| Por saltos | `saltos` |
| Por interpolación | `interpolacion` |
| Exponencial | `exponencial` |

Las implementaciones siguen el mismo esquema algorítmico en ambos lenguajes, con las adaptaciones necesarias para sus estructuras de datos. Los comentarios del código incluyen las fuentes de GeeksforGeeks utilizadas.

## Organización del repositorio

| Ruta | Contenido |
|---|---|
| `datos/` | Generador y archivos de entrada. |
| `java/src/` | Algoritmos, benchmarks, utilidades y pruebas de Java. |
| `python/` | Algoritmos, benchmarks, utilidades y pruebas de Python. |
| `resultados/` | Cuatro archivos CSV y descripción del entorno de ejecución. |
| `graficas/` | Nueve gráficas generadas desde los CSV. |
| `analisis/graficas.py` | Programa que genera las gráficas. |
| `ejecutar_todo.sh` | Automatización para Linux o WSL. |
| `.gitignore` | Exclusiones de archivos compilados y cachés. |

Los archivos `BenchmarkOrdenamiento.java`, `BenchmarkBusqueda.java` y sus equivalentes en Python ejecutan las mediciones. Los archivos `Ordenamiento.java`, `Busqueda.java`, `ordenamiento.py` y `busqueda.py` contienen los algoritmos.

## Requisitos

- JDK 21, con `java` y `javac` disponibles en la terminal.
- Python 3.10 o superior.
- Matplotlib para generar las gráficas.

La ejecución incluida utilizó Java 21.0.10 y Python 3.14.3 en Windows 11, con un Intel Core i5-13420H y 23,67 GiB de RAM detectada. El archivo `resultados/entorno.txt` debe registrar el entorno utilizado para obtener las mediciones.

## Ejecución en Windows con PowerShell

Ejecutar los comandos desde la carpeta que contiene `java`, `python`, `datos` y `resultados`. Mantener la misma terminal abierta durante el procedimiento para conservar las variables.

### 1. Comprobar el entorno

```powershell
$pythonTaller = "python"

java -version
javac -version
& $pythonTaller --version
```

`java` y `javac` deben corresponder al JDK 21. Si muestran versiones diferentes, corregir la configuración de la terminal antes de continuar.

Si `python` no identifica la instalación deseada, asignar su ruta completa a `$pythonTaller`.

Instalar Matplotlib:

```powershell
& $pythonTaller -m pip install matplotlib
```

### 2. Datos de entrada

El repositorio incluye los datos utilizados. No es necesario generarlos nuevamente.

Para regenerarlos:

```powershell
& $pythonTaller datos/generar_datos.py
```

El generador utiliza la semilla `2026` y los tamaños:

```text
1000, 10000, 100000 y 1000000
```

Para cada tamaño crea:

- `n_<n>_aleatorio.txt`: enteros de ocho dígitos, con posibles repeticiones.
- `n_<n>_ascendente.txt`: los mismos elementos ordenados ascendentemente.
- `n_<n>_descendente.txt`: los mismos elementos en orden descendente.
- `claves_n_<n>.txt`: 1.000 claves barajadas, con 500 presentes y 500 ausentes.

Java y Python leen los mismos archivos.

### 3. Compilar Java

```powershell
$fuentesTaller = (Get-ChildItem .\java\src\*.java).FullName

javac -encoding UTF-8 -d java/out $fuentesTaller
```

Continuar únicamente si la compilación termina sin errores.

### 4. Ejecutar las pruebas de corrección

```powershell
java -cp java/out Pruebas
& $pythonTaller python/pruebas.py
```

Cada programa debe mostrar:

```text
OK: 2000 casos aleatorios (6 ordenamientos + 6 búsquedas)
```

Estas pruebas comprueban la corrección de los algoritmos; las mediciones de rendimiento se ejecutan por separado.

### 5. Preparar una nueva ejecución

Los benchmarks agregan filas a los CSV existentes. Para repetir todo el experimento sin duplicar registros, ejecutar primero este bloque, que mueve los resultados y las gráficas anteriores a carpetas de respaldo junto a la carpeta del proyecto:

```powershell
$marcaTaller = Get-Date -Format "yyyyMMdd_HHmmss"

foreach ($carpetaTaller in @("resultados", "graficas")) {
    if (Test-Path ".\$carpetaTaller") {
        Move-Item ".\$carpetaTaller" `
            "..\${carpetaTaller}_anteriores_$marcaTaller"
    }

    New-Item -ItemType Directory `
        -Path ".\$carpetaTaller" | Out-Null
}
```

No ejecutar este bloque si solo se desea consultar los resultados incluidos.

Para las mediciones, mantener el equipo conectado a la corriente, desactivar temporalmente la suspensión y evitar ejecutar otras tareas intensivas. Ejecutar los benchmarks de forma secuencial.

### 6. Registrar el entorno

Ejecutar después de comprobar las versiones de Java y Python:

```powershell
$cpuTaller = Get-CimInstance Win32_Processor |
    Select-Object -First 1

$sistemaTaller = Get-CimInstance Win32_OperatingSystem
$equipoTaller = Get-CimInstance Win32_ComputerSystem

$ramTaller = [math]::Round(
    $equipoTaller.TotalPhysicalMemory / 1GB, 2
)

$versionJavaTaller = java -version 2>&1 |
    Select-Object -First 1

$versionPythonTaller = & $pythonTaller --version

@(
    "Fecha: $(Get-Date -Format o)"
    "CPU: $($cpuTaller.Name)"
    "Núcleos físicos: $($cpuTaller.NumberOfCores)"
    "Núcleos lógicos: $($cpuTaller.NumberOfLogicalProcessors)"
    "Memoria RAM: $ramTaller GiB"
    "SO: $($sistemaTaller.Caption)"
    "Versión del SO: $($sistemaTaller.Version)"
    "Java: $versionJavaTaller"
    "Python: $versionPythonTaller"
) | Set-Content .\resultados\entorno.txt -Encoding UTF8
```

### 7. Medir los ordenamientos

```powershell
$ordenamientosTaller = @(
    "insertion",
    "dualpivot",
    "merge",
    "heap",
    "radix",
    "bucket"
)

foreach ($algoritmoTaller in $ordenamientosTaller) {
    Write-Host "`nJAVA - $algoritmoTaller"

    java -cp java/out BenchmarkOrdenamiento `
        $algoritmoTaller datos resultados/ordenamiento_java.csv

    if ($LASTEXITCODE -ne 0) {
        throw "Falló la ejecución Java de $algoritmoTaller"
    }

    Write-Host "`nPYTHON - $algoritmoTaller"

    & $pythonTaller python/benchmark_ordenamiento.py `
        $algoritmoTaller datos resultados/ordenamiento_python.csv

    if ($LASTEXITCODE -ne 0) {
        throw "Falló la ejecución Python de $algoritmoTaller"
    }
}
```

Insertion Sort puede tardar varios minutos en los casos grandes. El bloque continúa automáticamente con los demás algoritmos.

### 8. Medir las búsquedas

```powershell
$busquedasTaller = @(
    "lineal",
    "binaria",
    "ternaria",
    "saltos",
    "interpolacion",
    "exponencial"
)

foreach ($algoritmoTaller in $busquedasTaller) {
    Write-Host "`nJAVA - $algoritmoTaller"

    java -cp java/out BenchmarkBusqueda `
        $algoritmoTaller datos resultados/busqueda_java.csv

    if ($LASTEXITCODE -ne 0) {
        throw "Falló la ejecución Java de $algoritmoTaller"
    }

    Write-Host "`nPYTHON - $algoritmoTaller"

    & $pythonTaller python/benchmark_busqueda.py `
        $algoritmoTaller datos resultados/busqueda_python.csv

    if ($LASTEXITCODE -ne 0) {
        throw "Falló la ejecución Python de $algoritmoTaller"
    }
}
```

### 9. Generar las gráficas

```powershell
& $pythonTaller analisis/graficas.py
```

Este comando lee los CSV y escribe nueve imágenes PNG en `graficas/`. No repite las mediciones.

### 10. Comprobar los archivos de resultados

```powershell
Get-ChildItem .\resultados\*.csv |
    ForEach-Object {
        [PSCustomObject]@{
            Archivo = $_.Name
            Filas = @(Import-Csv $_.FullName -Encoding UTF8).Count
        }
    }
```

Una ejecución completa debe producir:

| Archivo | Filas |
|---|---:|
| `ordenamiento_java.csv` | 72 |
| `ordenamiento_python.csv` | 72 |
| `busqueda_java.csv` | 96 |
| `busqueda_python.csv` | 96 |

El conteo comprueba la cantidad de registros; también deben revisarse las combinaciones de algoritmo, variante y tamaño para descartar duplicados o casos faltantes.

## Protocolo de medición

### Ordenamiento

Cada algoritmo procesa los cuatro tamaños y las entradas aleatoria, ascendente y descendente.

El benchmark lee los datos y prepara una copia nueva antes de iniciar cada medición. Después de ordenar, compara el resultado con el archivo ascendente de referencia. La lectura, la copia y la verificación quedan fuera del tiempo medido.

Java utiliza `System.nanoTime()` y realiza un calentamiento previo por configuración. Python utiliza `time.perf_counter_ns()`; su benchmark no incluye un calentamiento separado. Ambos calculan el promedio y la desviación estándar muestral de cinco repeticiones completas.

### Búsqueda

Los benchmarks utilizan arreglos ascendentes y cuatro variantes:

| Variante | Consultas |
|---|---|
| `claves_mixtas` | Lote de 500 claves presentes y 500 ausentes. |
| `pos_inicio` | 1.000 consultas de la clave situada al inicio. |
| `pos_centro` | 1.000 consultas de la clave situada en el centro. |
| `pos_final` | 1.000 consultas de la clave situada al final. |

Cada repetición mide un lote de 1.000 búsquedas. El programa divide el tiempo total entre 1.000 y reporta el promedio por búsqueda.

La comprobación de los índices devueltos queda fuera de la medición. Java realiza un calentamiento previo por configuración.

Estos archivos no incluyen una medición de búsqueda lineal sobre arreglos desordenados.

## Casos estimados y límites de ejecución

Antes de ejecutar un tamaño mayor, el benchmark de ordenamiento calcula una predicción a partir de una medición menor y del crecimiento teórico correspondiente. Si la predicción supera cinco minutos por ejecución, registra el caso como `estimado`.

El programa también registra estimaciones cuando detecta un `StackOverflowError` en Java, un `RecursionError` en Python o una ejecución que supera el límite establecido.

La regla no funciona como un temporizador que interrumpe el algoritmo al cumplirse cinco minutos. La ejecución en curso puede superar ese tiempo antes de devolver el control al benchmark.

Los registros estimados incluyen la explicación en `observacion`; sus columnas de repeticiones y desviación quedan vacías. Un tiempo estimado no equivale a una medición completada.

La implementación de Dual-Pivot QuickSort selecciona el primer y el último elemento como pivotes. En entradas ordenadas puede producir particiones desequilibradas y alcanzar los límites de recursión.

## Formato de los resultados

Cada CSV contiene:

```text
algoritmo, lenguaje, variante, n,
rep1, rep2, rep3, rep4, rep5,
promedio, desviacion, tipo, observacion
```

Los nombres reales de las columnas incluyen la unidad:

- Ordenamiento: milisegundos, con sufijo `_ms`.
- Búsqueda: nanosegundos por búsqueda, con sufijo `_ns`.

La columna `tipo` distingue `medido` y `estimado`.

La ejecución incluida contiene:

| Archivo | Medidos | Estimados | Total |
|---|---:|---:|---:|
| `ordenamiento_java.csv` | 68 | 4 | 72 |
| `ordenamiento_python.csv` | 63 | 9 | 72 |
| `busqueda_java.csv` | 96 | 0 | 96 |
| `busqueda_python.csv` | 96 | 0 | 96 |

Otra ejecución puede producir una distribución diferente de casos medidos y estimados, según el rendimiento del equipo y sus límites de ejecución.

## Gráficas

| Archivo | Comparación |
|---|---|
| `g1_crecimiento_ordenamiento_java.png` | Crecimiento de los ordenamientos en Java, entrada aleatoria. |
| `g2_crecimiento_ordenamiento_python.png` | Crecimiento de los ordenamientos en Python, entrada aleatoria. |
| `g3_orden_entrada_java_n1000.png` | Orden de entrada en Java, n = 1.000. |
| `g4_orden_entrada_java_n10000.png` | Orden de entrada en Java, n = 10.000. |
| `g5_orden_entrada_java_n100000.png` | Orden de entrada en Java, n = 100.000. |
| `g6_compilado_vs_interpretado_ordenamiento_n1000000.png` | Java frente a Python, ordenamiento de entrada aleatoria, n = 1.000.000. |
| `g7_crecimiento_busqueda_java.png` | Crecimiento de las búsquedas en Java, claves mixtas. |
| `g8_crecimiento_busqueda_python.png` | Crecimiento de las búsquedas en Python, claves mixtas. |
| `g9_compilado_vs_interpretado_busqueda_n1000000.png` | Java frente a Python, búsquedas con claves mixtas, n = 1.000.000. |

Todas utilizan una escala logarítmica para el tiempo. Las gráficas de crecimiento también utilizan escala logarítmica para el tamaño del arreglo. Las estimaciones aparecen con marcadores huecos y líneas discontinuas, o con barras rayadas.

## Ejecución individual desde un IDE

También es posible ejecutar los benchmarks desde IntelliJ u otro editor configurando sus argumentos y el directorio de trabajo.

Ejemplo para Java:

```text
Clase principal: BenchmarkOrdenamiento
Argumentos: merge datos resultados/ordenamiento_java.csv
Directorio de trabajo: raíz del proyecto
JDK: 21
```

Ejemplo para Python:

```text
Archivo: python/benchmark_ordenamiento.py
Argumentos: merge datos resultados/ordenamiento_python.csv
Directorio de trabajo: raíz del proyecto
```

Estas ejecuciones también agregan filas al CSV indicado. Para una prueba independiente, utilizar otro archivo de salida.

## Linux y WSL

El archivo `ejecutar_todo.sh` automatiza las mediciones y utiliza herramientas de Linux para registrar el entorno.

```bash
bash ejecutar_todo.sh
python3 analisis/graficas.py
```

Requiere el JDK, Python y Matplotlib instalados dentro de ese entorno. El script elimina los cuatro CSV existentes antes de iniciar; guardar una copia si se desean conservar.

## Interpretación y reproducibilidad

Los tiempos dependen del equipo, las versiones de los lenguajes, la compilación JIT, la gestión de memoria y la actividad del sistema. Las conclusiones deben referirse a las implementaciones y condiciones evaluadas.

Conservar las cinco repeticiones y su desviación permite reconocer la variabilidad. No deben eliminarse valores altos únicamente para reducir el promedio.

El informe académico se prepara por separado utilizando los CSV, las gráficas y el entorno registrado.

## Archivos excluidos

El `.gitignore` excluye:

```gitignore
java/out/
__pycache__/
*.pyc
```

Las carpetas de respaldo de ejecuciones anteriores deben mantenerse fuera del repositorio que se entrega.