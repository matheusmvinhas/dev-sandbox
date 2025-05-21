from pyspark.sql import SparkSession
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = "8123"
CLICKHOUSE_DB = "metrics"
CLICKHOUSE_USER = "default"
CLICKHOUSE_PASSWORD = ""
CLICKHOUSE_TABLE = "pydeequ_verification_results"

# Configura Spark
spark = SparkSession.builder \
    .appName("Load PyDeequ Metrics to ClickHouse") \
    .config("spark.driver.extraClassPath", "/app/spark-jars/*") \
    .config("spark.executor.extraClassPath", "/app/spark-jars/*") \
    .getOrCreate()

# Lê os arquivos Parquet
df = spark.read.parquet('/app/data/output/metrics_pydeequ/check_result')

# JDBC URL
CLICKHOUSE_HOST = "dev-sandbox-clickhouse-1"
CLICKHOUSE_PORT = "8123"
CLICKHOUSE_DB = "metrics"

jdbc_url = "jdbc:clickhouse://dev-sandbox-clickhouse-1:8123/metrics"

# Escreve na tabela ClickHouse com overwrite
print(f"Escrevendo na tabela {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE} via {jdbc_url}")
df.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", CLICKHOUSE_TABLE) \
    .option("user", CLICKHOUSE_USER) \
    .option("password", CLICKHOUSE_PASSWORD) \
    .mode("append") \
    .save()

print("Carga concluída com sucesso!")

spark.stop()