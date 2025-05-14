
from pyspark.sql import SparkSession
# from utils.SparkHelper import SessionBuilder

spark = SparkSession.builder \
    .appName("ETL-Job-teste") \
    .master("local[*]") \
    .getOrCreate()

spark.read.csv(
    "/app/data/teste.csv",
    header=True,
    inferSchema=True,
).printSchema()

spark.read.csv(
    "/app/data/teste.csv",
    header=True,
    inferSchema=True,
).select("dataColeta").write.mode("overwrite").csv("/app/data/output", header=True)

spark.stop()