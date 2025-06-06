
from utils.SparkHelper import SessionBuilder
# from utils.SparkHelper import SessionBuilder

spark = (
    SessionBuilder.get_builder().appName("teste")
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.adaptive.coalescePartitions.parallelismFirst", "false")
    .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "200MB")
    .config("spark.sql.adaptive.coalescePartitions.minPartitionSize", "128MB")
    .config("spark.sql.shuffle.partitions", 200)
    .getOrCreate()
)

spark.read.csv(
    "s3a://ip-byte-pool/raw/exemple/teste.csv",
    header=True,
    inferSchema=True,
).printSchema()

spark.read.csv(
    "s3a://ip-byte-pool/raw/exemple/teste.csv",
    header=True,
    inferSchema=True,
).select("dataColeta").write.mode("overwrite").csv("s3a://ip-byte-pool/output/exemple/", header=True)

spark.stop()
