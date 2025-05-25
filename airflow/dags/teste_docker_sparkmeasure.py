from airflow import DAG
from datetime import datetime, timedelta
from custom_operators.custom_docker_operator import CustomDockerOperator


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

    run_local_spark = CustomDockerOperator(
        task_id='run_spark_sparkmeasure_local',
        command="spark-submit --master local[*] /app/scripts/exemple/teste_sparkmeasure_etl.py"
    )

    run_local_spark_load = CustomDockerOperator(
        task_id='run_load_sparkmeasure_metrics',
        command="spark-submit --master local[*] /app/scripts/exemple/load_sparkmeasure_metrics.py"
    )

    run_local_spark >> run_local_spark_load

    