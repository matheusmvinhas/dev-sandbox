#!/bin/bash
set -e

# Configura o alias
mc alias set local http://localhost:9002 minio minio123

# Configuração
BUCKETS=("spark-events" "ip-byte-pool/raw")
RETENTION_DAYS=7

for BUCKET in "${BUCKETS[@]}"; do
    echo "Limpando arquivos com mais de $RETENTION_DAYS dias no bucket: $BUCKET"
    mc find local/$BUCKET --older-than ${RETENTION_DAYS}d --exec "mc rm {}"
done

echo "Limpeza de arquivos antigos concluída!"