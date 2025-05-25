#!/bin/bash

# Exporta o PYTHONPATH para garantir que o processo do Airflow tenha visibilidade
export PYTHONPATH="/opt/airflow:/opt/airflow/utils:/opt/airflow/custom_operators"

echo "[entrypoint] PYTHONPATH set to: $PYTHONPATH"

# Executa o comando original passado ao container
exec "$@"