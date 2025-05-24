from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="local_spark_etl",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["spark", "local"],
) as dag:

    # run_local_spark = BashOperator(
    #     task_id="run_spark_local",
    #     bash_command=(
    #         "docker exec dev-sandbox-etl-runner-1 "
    #         "spark-submit "
    #         "--master local[*] "
    #         "/app/scripts/exemple/teste_spark_etl.py"
    #     ),
    # )

    run_local_spark = BashOperator(
        task_id="run_spark_pydeequ_local",
        bash_command=(
            "docker exec -e SPARK_VERSION=3.5 etl-runner "
            "spark-submit "
            "--master local[*] "
            "/app/scripts/exemple/pydeequ_exemple.py"
        ),
    do_xcom_push=False
    )