FROM apache/airflow:3.0.0-python3.11

USER root
RUN apt-get update && apt-get install -y gcc g++ libpq-dev

USER airflow
COPY requirements-airflow.txt /requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /requirements.txt