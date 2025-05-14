from pyspark.sql import SparkSession

class SessionBuilder():

    @classmethod
    def get_builder(cls):

        builder = SparkSession.builder.master("local[*]")

        packages = [
            "org.apache.hadoop:hadoop-aws:3.3.4",
            "com.amazonaws:aws-java-sdk-bundle:1.12.262",
            "io.dataflint:spark_2.12:0.3.2",
            "io.delta:delta-spark_2.12:3.2.1",
            "com.clickhouse:clickhouse-jdbc:0.7.2",
            "org.apache.httpcomponents.client5:httpclient5:5.2.1",
            "org.apache.httpcomponents.core5:httpcore5:5.2.1",
        ]

        plugins = [
            "io.dataflint.spark.SparkDataflintPlugin"
        ]

        extensions = [
            "io.delta.sql.DeltaSparkSessionExtension"
        ]

        configs = {
            "spark.hadoop.fs.s3a.aws.credentials.provider": "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.jars.packages": ",".join(packages),
            "spark.plugins": ",".join(plugins),
            "spark.sql.extensions": ",".join(extensions),
            "spark.driver.memory": "5G",
            "spark.memory.fraction": 0.8,
            "spark.memory.storageFraction": 0.2,
            "spark.local.dir": "/tmp/spark/",
            "spark.sql.warehouse.dir": "/tmp/spark/spark-warehouse/",
            "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        }

        for param, setting in configs.items():
            builder = builder.config(param, setting)

        return builder