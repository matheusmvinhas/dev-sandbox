#!/bin/bash
set -e

mc alias set local http://localhost:9002 minio minio123

BUCKET="ip-byte-pool"
PREFIX="output/"

echo "Limpando arquivos do prefixo: $PREFIX no bucket: $BUCKET"
mc rm --recursive --force local/$BUCKET/$PREFIX

echo "Limpeza seletiva concluída!"