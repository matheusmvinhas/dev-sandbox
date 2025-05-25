
import subprocess
from utils.SparkHelper import SessionBuilder

# ✅ Variáveis de conexão ClickHouse
CLICKHOUSE_HOST = "clickhouse"            # Altere conforme sua infra
CLICKHOUSE_PORT = 9000                   # Porta padrão
CLICKHOUSE_USER = "default"              # Usuário padrão
CLICKHOUSE_PASSWORD = ""                 # Senha se tiver
CLICKHOUSE_DB = "metrics"                # Banco de dados

# ✅ Variáveis de conexão JDBC
JDBC_PORT = 8123                         # Porta para JDBC HTTP
jdbc_url = f"jdbc:clickhouse://clickhouse:{JDBC_PORT}/{CLICKHOUSE_DB}"

# ✅ Diretório de Parquet e mapeamento tabela -> caminho
tables = [
    ("agg_stg_metrics", "s3a://ip-byte-pool/metrics/metrics_sparkMeasure/agg_stagemetrics"),
    ("agg_task_metrics", "s3a://ip-byte-pool/metrics/metrics_sparkMeasure/agg_taskmetrics"),
    ("stg_metrics", "s3a://ip-byte-pool/metrics/metrics_sparkMeasure/stagemetrics"),
    ("task_metrics", "s3a://ip-byte-pool/metrics/metrics_sparkMeasure/taskmetrics")
]

# ✅ Criação da SparkSession
spark = SessionBuilder.get_builder() \
    .appName("Spark ClickHouse ETL") \
    .getOrCreate()

# ✅ Loop sobre todas as tabelas
for CLICKHOUSE_TABLE, parquet_path in tables:
    
    # ✅ Passo 1: TRUNCATE usando clickhouse-client via subprocess
    print(f"🔸 Truncating table {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE} via clickhouse-client...")
    
    truncate_cmd = [
        "clickhouse-client",
        "--host", CLICKHOUSE_HOST,
        "--port", str(CLICKHOUSE_PORT),
        "--user", CLICKHOUSE_USER,
        "--password", CLICKHOUSE_PASSWORD,
        "--query", f"TRUNCATE TABLE {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}"
    ]
    
    try:
        subprocess.run(truncate_cmd, check=True)
        print(f"✅ Tabela {CLICKHOUSE_TABLE} truncada com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao truncar a tabela {CLICKHOUSE_TABLE}: {e}")
        continue  # Pula para a próxima tabela

    # ✅ Passo 2: Leitura do arquivo Parquet
    print(f"🔸 Lendo arquivo Parquet de {parquet_path}")
    df = spark.read.parquet(parquet_path)
    print(f"✅ Leitura concluída para {CLICKHOUSE_TABLE}")

    # ✅ Passo 3: Escrita no ClickHouse via JDBC
    print(f"🔸 Escrevendo na tabela {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE} via {jdbc_url}")
    try:
        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", CLICKHOUSE_TABLE) \
            .option("user", CLICKHOUSE_USER) \
            .option("password", CLICKHOUSE_PASSWORD) \
            .mode("append") \
            .save()

        print(f"✅ Carga concluída com sucesso para {CLICKHOUSE_TABLE}!")
    except Exception as e:
        print(f"❌ Erro ao carregar dados na tabela {CLICKHOUSE_TABLE}: {e}")

# ✅ Finaliza SparkSession
spark.stop()
print("✅ Processo de ETL concluído para todas as tabelas.")