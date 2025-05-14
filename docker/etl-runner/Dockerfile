FROM bitnami/spark:3.5.0

USER root
RUN install_packages python3 python3-pip libpq-dev gcc g++

# Instala as libs Python necessárias
RUN pip install --upgrade pip && \
    pip install pandas duckdb psycopg2-binary delta-spark==2.4.0

# Cria diretório de trabalho
WORKDIR /app
CMD ["tail", "-f", "/dev/null"]