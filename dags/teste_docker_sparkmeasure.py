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
    dag_id='local_spark_etl_sparkMeasure_docker',
    default_args=default_args,
    description='Run local Spark ETL with sparkmeasure using DockerOperator',
    schedule=None,
    start_date= datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'docker', 'sparkmeasure'],
) as dag:

    run_local_spark = DockerOperator(
        task_id='run_spark_sparkmeasure_local',
        image='dev-sandbox-etl-runner:latest',
        api_version='auto',
        auto_remove='success',
        command="spark-submit --master local[*] /app/etl/teste_sparkmeasure_etl.py",
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        environment={"SPARK_VERSION": "3.5"},
        mounts=[
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/etl", target="/app/etl", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/data", target="/app/data", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/utils", target="/app/utils", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/spark-events", target="/tmp/spark-events", type="bind"),
        Mount(source='/Users/matheusvinhas/projects/dev-sandbox/spark-jars', target='/app/spark-jars', type='bind')
        ],
        tty=False,
        mount_tmp_dir=False,
        execution_timeout=timedelta(minutes=10),
    )

    run_local_spark_load = DockerOperator(
        task_id='run_load_spark_sparkmeasure_local',
        image='dev-sandbox-etl-runner:latest',
        api_version='auto',
        auto_remove='success',
        command="spark-submit --master local[*] /app/etl/load_sparkmeasure_metrics.py",
        docker_url='unix://var/run/docker.sock',
        network_mode='dev-sandbox_default',
        environment={"SPARK_VERSION": "3.5"},
        mounts=[
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/etl", target="/app/etl", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/data", target="/app/data", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/utils", target="/app/utils", type="bind"),
        Mount(source="/Users/matheusvinhas/projects/dev-sandbox/spark-events", target="/tmp/spark-events", type="bind"),
        Mount(source='/Users/matheusvinhas/projects/dev-sandbox/spark-jars', target='/app/spark-jars', type='bind')
        ],
        tty=False,
        mount_tmp_dir=False,
        execution_timeout=timedelta(minutes=10),
    )

    run_local_spark >> run_local_spark_load

    