#!/bin/bash
set -e

# Configura o alias
mc alias set local http://localhost:9002 minio minio123

# Lista de buckets para limpar
BUCKETS=("spark-events" "ip-byte-pool")

for BUCKET in "${BUCKETS[@]}"; do
    echo "Limpando completamente o bucket: $BUCKET"
    mc rm --recursive --force local/$BUCKET || true
done

echo "Limpeza completa concluída!"