#!/bin/bash

PACKAGES=(
  "org.apache.hadoop:hadoop-aws:3.3.4"
  "com.amazonaws:aws-java-sdk-bundle:1.12.262"
  "io.dataflint:spark_2.12:0.3.2"
  "io.delta:delta-spark_2.12:3.2.1"
  "com.clickhouse:clickhouse-jdbc:0.7.2"
  "org.apache.httpcomponents.client5:httpclient5:5.2.1"
  "org.apache.httpcomponents.core5:httpcore5:5.2.1"
)

PACKAGE_STRING=$(IFS=, ; echo "${PACKAGES[*]}")

echo "📦 Baixando pacotes Spark..."
mkdir -p spark-jars

# Usamos --packages para forçar download e pegamos o Ivy cache
spark-submit \
  --packages "$PACKAGE_STRING" \
  --verbose \
  2>&1 | grep -Eo 'https://[^ ]+\.jar' | sort -u > spark-jars/urls.txt

echo "📁 Baixando arquivos JAR..."
cd spark-jars
wget -nc -i urls.txt
cd ..

echo "✅ JARs baixados com sucesso na pasta spark-jars/"