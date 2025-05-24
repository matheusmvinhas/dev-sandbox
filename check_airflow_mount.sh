#!/bin/bash

echo "🔍 Verificando diretório atual..."
pwd

echo "🔍 Verificando se está na raiz do projeto (dev-sandbox)..."
if [ ! -d "./airflow" ]; then
  echo "❌ Diretório 'airflow/' não encontrado no local atual."
  echo "➡️  Por favor, rode este script a partir do diretório raiz do projeto: ~/projects/dev-sandbox"
  exit 1
else
  echo "✅ Diretório 'airflow/' encontrado."
fi

echo "🔍 Verificando se 'airflow/dags/' existe..."
if [ ! -d "./airflow/dags" ]; then
  echo "❌ Diretório 'airflow/dags/' não encontrado."
  exit 1
else
  echo "✅ Diretório 'airflow/dags/' encontrado."
fi

echo "🔍 Listando arquivos em 'airflow/dags/'..."
ls -la ./airflow/dags

echo "🔍 Verificando permissões dos arquivos..."
find ./airflow/dags -type f -exec ls -l {} \;

echo "🔍 Verificando se o Docker container 'airflow' está rodando..."
if ! docker ps --format '{{.Names}}' | grep -q "^airflow$"; then
  echo "❌ Container 'airflow' não está rodando."
  exit 1
else
  echo "✅ Container 'airflow' está rodando."
fi

echo "🔍 Listando conteúdo do diretório de DAGs dentro do container..."
docker exec -it airflow ls -la /opt/airflow/dags

echo "🔍 Listando DAGs reconhecidas pelo Airflow..."
docker exec -it airflow airflow dags list

echo "✅ Diagnóstico concluído!"
