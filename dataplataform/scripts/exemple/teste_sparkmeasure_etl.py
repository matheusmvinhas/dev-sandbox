
from utils.SparkHelper import SessionBuilder
from sparkmeasure import TaskMetrics, StageMetrics
from pyspark.sql.functions import lit, current_timestamp
import uuid
from datetime import date
import random



spark = (
    SessionBuilder.get_builder().appName("teste")
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.adaptive.coalescePartitions.parallelismFirst", "false")
    .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "200MB")
    .config("spark.sql.adaptive.coalescePartitions.minPartitionSize", "128MB")
    .config("spark.sql.shuffle.partitions", 200)
    .getOrCreate()
)
execution_date = date.today().strftime("%Y-%m-%d")
execution_id = str(uuid.uuid4())
execution_ts = current_timestamp()
tabela_referente = "teste"

def add_execution_columns(df, tabela_referente, execution_date=None, execution_id=None, execution_ts=None):
    return df.withColumn("tabela_referente", lit(tabela_referente)) \
             .withColumn("execution_date", lit(execution_date).cast("date")) \
             .withColumn("execution_id", lit(execution_id)) \
             .withColumn("execution_ts", lit(execution_ts))


taskmetrics = TaskMetrics(spark)
stagemetrics = StageMetrics(spark)
taskmetrics.begin()
stagemetrics.begin()

range1 = random.randint(500, 1500)
range2 = random.randint(500, 1500)
range3 = random.randint(500, 1500)

query = f"""
    SELECT COUNT(*)
    FROM range({range1})
    CROSS JOIN range({range2})
    CROSS JOIN range({range3})
"""

df = spark.sql(query)
df.show()
taskmetrics.end()
stagemetrics.end()

task_metrics_df = add_execution_columns(taskmetrics.create_taskmetrics_DF(),tabela_referente, execution_date, execution_id, execution_ts)
agg_task_metrics_df = add_execution_columns(taskmetrics.aggregate_taskmetrics_DF(),tabela_referente, execution_date, execution_id, execution_ts)
stg_metrics_df = add_execution_columns(stagemetrics.create_stagemetrics_DF(),tabela_referente, execution_date, execution_id, execution_ts)
agg_stg_metrics_df = add_execution_columns(stagemetrics.aggregate_stagemetrics_DF(),tabela_referente, execution_date, execution_id, execution_ts)


task_metrics_df.repartition(1).write.mode('append').format('parquet').save('s3a://ip-byte-pool/metrics/metrics_sparkMeasure/taskmetrics')
agg_task_metrics_df.repartition(1).write.mode('append').format('parquet').save('s3a://ip-byte-pool/metrics/metrics_sparkMeasure/agg_taskmetrics')

stg_metrics_df.repartition(1).write.mode('append').format('parquet').save('s3a://ip-byte-pool/metrics/metrics_sparkMeasure/stagemetrics')
agg_stg_metrics_df.repartition(1).write.mode('append').format('parquet').save('s3a://ip-byte-pool/metrics/metrics_sparkMeasure/agg_stagemetrics')


spark.stop()