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
    dag_id='local_spark_etl_docker',
    default_args=default_args,
    description='Run local Spark ETL with PyDeequ using DockerOperator',
    schedule=None,
    start_date= datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'docker', 'pydeequ'],
) as dag:

    run_local_spark = CustomDockerOperator(
        task_id='run_spark_pydeequ_local',
        command="spark-submit --master local[*] /app/scripts/exemple/pydeequ_exemple.py"
    )

    run_local_spark_load = CustomDockerOperator(
        task_id='run_load_spark_pydeequ_local',
        command="spark-submit --master local[*] /app/scripts/exemple/load_pydeequ_metrics.py"
    )

    run_local_spark >> run_local_spark_load

    