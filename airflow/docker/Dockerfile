FROM apache/airflow:3.0.0-python3.11

USER root
RUN apt-get update && apt-get install -y gcc g++ libpq-dev
COPY airflow/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


USER airflow
COPY airflow/requirements-airflow.txt /requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /requirements.txt

# Mantém a definição no ENV para herdar na build (boa prática)
ENV PYTHONPATH="/opt/airflow:/opt/airflow/utils:/opt/airflow/custom_operators"

# Define o entrypoint customizado
ENTRYPOINT ["/entrypoint.sh"]
