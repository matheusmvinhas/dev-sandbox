FROM bitnami/spark:3.5.5

USER root
RUN install_packages python3 python3-pip libpq-dev gcc g++


# Copia requirements isolado
COPY requirements-spark.txt /tmp/requirements.txt

# Instala libs extras
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get update && apt-get install -y clickhouse-client

ENV SPARK_VERSION=3.5

COPY spark-jars/ /opt/bitnami/spark/jars/

# Cria diretório de trabalho
WORKDIR /app