
from utils.SparkHelper import SessionBuilder
from datetime import date
import sys
from pyspark.sql.functions import lit, current_timestamp
import uuid

spark = (
    SessionBuilder.get_builder().appName("pydeequ_exemple")
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.adaptive.coalescePartitions.parallelismFirst", "false")
    .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "200MB")
    .config("spark.sql.adaptive.coalescePartitions.minPartitionSize", "128MB")
    .config("spark.sql.shuffle.partitions", 200)
    .getOrCreate()
)


execution_date = date.today().strftime("%Y-%m-%d")

df = spark.read.csv(
    "s3a://ip-byte-pool/raw/exemple/teste.csv",
    header=True,
    inferSchema=True,
)

from pydeequ.repository import FileSystemMetricsRepository, ResultKey

metrics_file = f"s3a://ip-byte-pool/metrics/metrics_pydeequ/repository/exemple_metrics.json"
exemple_repository = FileSystemMetricsRepository(spark, path = metrics_file)

key_tags = {"tag": f"exemple_{execution_date}"}
resultKey = ResultKey(spark, ResultKey.current_milli_time(), key_tags)

verify_key_tag = {"tag": f"verify_exemple_{execution_date}"}
verify_resultKey = ResultKey(spark, ResultKey.current_milli_time(), verify_key_tag)

execution_id = str(uuid.uuid4())
execution_ts = current_timestamp()
tabela_referente = "teste" 

from pydeequ.analyzers import *

analysisResult = AnalysisRunner(spark) \
                    .onData(df) \
                    .addAnalyzer(Size()) \
                    .addAnalyzer(Completeness("dataColeta")) \
                    .addAnalyzer(Completeness("produtoIdentificador")) \
                    .addAnalyzer(Completeness("lojaDescricao")) \
                    .addAnalyzer(Distinctness("produtoIdentificador")) \
                    .addAnalyzer(Uniqueness(["dataColeta", "produtoIdentificador", "lojaDescricao"])) \
                    .addAnalyzer(Compliance("lojaDescricao", "lojaDescricao in ('ATACADAO_91001')")) \
                    .addAnalyzer(Maximum("precoTratado")) \
                    .useRepository(exemple_repository) \
                    .saveOrAppendResult(resultKey) \
                    .run()

from pydeequ.checks import *
from pydeequ.verification import *

check = Check(spark, CheckLevel.Warning, "Exemple Check") \

checkResult = VerificationSuite(spark) \
    .onData(df) \
    .addCheck(
        check.isComplete("dataColeta")  \
        .isComplete("produtoIdentificador")  \
        .isComplete("lojaDescricao")  \
        .hasUniqueness(["dataColeta", "produtoIdentificador", "lojaDescricao"], assertion=lambda x: x==1) \
        .hasCompleteness("produtoIdentificador", assertion=lambda x: x >= 0.95) \
        .isNonNegative("precoTratado")) \
        .useRepository(exemple_repository) \
        .saveOrAppendResult(verify_resultKey) \
    .run()

checkResult_df = VerificationResult.checkResultsAsDataFrame(spark, checkResult)
checkResult_df = checkResult_df \
    .withColumn("execution_id", lit(execution_id)) \
    .withColumn("execution_ts", execution_ts) \
    .withColumn("tabela_referente", lit(tabela_referente))
checkResult_df.repartition(1).write.mode('append').format('parquet').save("s3a://ip-byte-pool/metrics/metrics_pydeequ/check_result/")

print("ETL PyDeequ finalizado com sucesso!")
spark.sparkContext._gateway.shutdown_callback_server()
spark.stop()
sys.exit(0)
