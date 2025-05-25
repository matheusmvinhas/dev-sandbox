#!/bin/sh

set -e

# Espera o MinIO iniciar
echo "Aguardando MinIO aceitar comandos mc..."
until mc alias set local http://minio:9000 minio minio123 && mc ls local > /dev/null 2>&1; do
  echo "MinIO ainda não está pronto..."
  sleep 1
done

echo "MinIO na porta 9000!"

# Configura o mc
mc alias set local http://minio:9000 minio minio123

# Aguarda o MinIO estar totalmente pronto para comandos
echo "Aguardando MinIO aceitar comandos mc..."
until mc ls local > /dev/null 2>&1; do
  echo "Aguardando disponibilidade do MinIO para mc..."
  sleep 1
done

echo "MinIO pronto para mc!"

# Cria buckets e sincroniza dados
if [ -f /buckets.txt ]; then
  while IFS= read -r bucket; do
    if [ -n "$bucket" ]; then
      # Cria o bucket se não existir
      if ! mc ls local/$bucket > /dev/null 2>&1; then
        echo "Criando bucket: $bucket"
        mc mb local/$bucket
      else
        echo "Bucket $bucket já existe"
      fi

      # Sincroniza, se houver pasta correspondente no staging
      if [ -d "/staging/$bucket" ]; then
        if [ "$(ls -A /staging/$bucket)" ]; then
          echo "Sincronizando /staging/$bucket para local/$bucket..."
          mc mirror --overwrite /staging/$bucket local/$bucket
        else
          echo "Pasta /staging/$bucket está vazia, nada para sincronizar."
        fi
      else
        echo "Nenhuma pasta de staging para $bucket"
      fi
    fi
  done < /buckets.txt
else
  echo "Arquivo buckets.txt não encontrado!"
  exit 1
fi

echo "MinIO Init finalizado com sucesso!"