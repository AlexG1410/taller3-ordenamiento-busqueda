#!/usr/bin/env bash
# Ejecuta todo el taller: genera datos (si faltan), compila, mide y deja los CSV en resultados/.
# Cada algoritmo se mide en un proceso (JVM / intérprete) independiente, en serie, nunca en paralelo.
set -euo pipefail
cd "$(dirname "$0")"

R=resultados
mkdir -p "$R"

if [ ! -f datos/n_1000000_aleatorio.txt ]; then
  python3 datos/generar_datos.py
fi

javac -encoding UTF-8 -d java/out java/src/*.java

{
  echo "Fecha: $(date -Iseconds)"
  echo "CPU: $(lscpu | grep 'Model name' | sed 's/Model name:\s*//')"
  echo "Núcleos: $(nproc)"
  echo "Memoria: $(free -h | awk '/Mem:/{print $2}')"
  echo "SO: $(uname -srm)"
  echo "Java: $(java -version 2>&1 | grep -i 'openjdk version\|java version')"
  echo "Python: $(python3 --version)"
} > "$R/entorno.txt"

ORDEN="merge heap radix bucket dualpivot insertion"
BUSQ="lineal binaria ternaria saltos interpolacion exponencial"
JAVA="java -Dstdout.encoding=UTF-8 -cp java/out"

rm -f "$R"/ordenamiento_java.csv "$R"/busqueda_java.csv "$R"/ordenamiento_python.csv "$R"/busqueda_python.csv

for a in $BUSQ; do $JAVA BenchmarkBusqueda "$a" datos "$R/busqueda_java.csv"; done 2>&1 | grep -v JAVA_TOOL | tee "$R/log_busqueda_java.txt"
for a in $ORDEN; do $JAVA BenchmarkOrdenamiento "$a" datos "$R/ordenamiento_java.csv"; done 2>&1 | grep -v JAVA_TOOL | tee "$R/log_ordenamiento_java.txt"
for a in $BUSQ; do python3 python/benchmark_busqueda.py "$a" datos "$R/busqueda_python.csv"; done 2>&1 | tee "$R/log_busqueda_python.txt"
for a in $ORDEN; do python3 python/benchmark_ordenamiento.py "$a" datos "$R/ordenamiento_python.csv"; done 2>&1 | tee "$R/log_ordenamiento_python.txt"

echo "FIN $(date -Iseconds)" | tee -a "$R/entorno.txt"
