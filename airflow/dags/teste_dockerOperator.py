from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import timedelta
from datetime import datetime
from docker.types import Mount

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='local_spark_etl_docker',
    default_args=default_args,
    description='Run local Spark ETL with PyDeequ using DockerOperator',
    schedule=None,
    start_date= datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'docker', 'pydeequ'],
) as dag:

    run_local_spark = DockerOperator(
        task_id='run_spark_pydeequ_local',
        image='dev-sandbox-etl-runner:latest',
        api_version='auto',
        auto_remove='success',
        command="spark-submit --master local[*] /app/scripts/exemple/pydeequ_exemple.py",
        docker_url='unix://var/run/docker.sock',
        network_mode='orchestration_dev-sandbox',
        environment={
            "SPARK_VERSION": "3.5",
            "MINIO_ENDPOINT": "http://minio:9000",
            "MINIO_ACCESS_KEY": "minio",
            "MINIO_SECRET_KEY": "minio123",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123"
        },
        mounts=[
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/scripts", target="/app/scripts", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/utils", target="/app/utils", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/minIo/staging/spark-events", target="/tmp/spark-events", type="bind"),
        Mount(source='/Users/matheusvinhas/projects/dev-sandbox/dataplataform/spark-jars', target='/app/spark-jars', type='bind')
        ],
        tty=False,
        mount_tmp_dir=False,
        execution_timeout=timedelta(minutes=10),
    )

    run_local_spark_load = DockerOperator(
        task_id='run_load_spark_pydeequ_local',
        image='dev-sandbox-etl-runner:latest',
        api_version='auto',
        auto_remove='success',
        command="spark-submit --master local[*] /app/scripts/exemple/load_pydeequ_metrics.py",
        docker_url='unix://var/run/docker.sock',
        network_mode='orchestration_dev-sandbox',
        environment={
            "SPARK_VERSION": "3.5",
            "MINIO_ENDPOINT": "http://minio:9000",
            "MINIO_ACCESS_KEY": "minio",
            "MINIO_SECRET_KEY": "minio123",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123"
        },
        mounts=[
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/scripts", target="/app/scripts", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/utils", target="/app/utils", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/minIo/staging/spark-events", target="/tmp/spark-events", type="bind"),
        Mount(source='/Users/matheusvinhas/projects/dev-sandbox/dataplataform/spark-jars', target='/app/spark-jars', type='bind')
        ],
        tty=False,
        mount_tmp_dir=False,
        execution_timeout=timedelta(minutes=10),
    )

    run_local_spark >> run_local_spark_load

    