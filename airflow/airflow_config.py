from datetime import timedelta

# Configurações padrão para DAGs
DEFAULT_DAG_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Timezone padrão
TIMEZONE = 'America/Sao_Paulo'

# Intervalo de execução padrão
DEFAULT_SCHEDULE_INTERVAL = '@daily'

# Tags padrão para DAGs
DEFAULT_TAGS = ['dataplatform', 'sandbox']

# Conexão S3/MinIO
S3_CONN_ID = 'minio_s3'
S3_BUCKET = 'sandbox-bucket'
S3_ENDPOINT_URL = 'http://minio:9000'

# Outras configurações de infraestrutura
SPARK_IMAGE = 'dev-sandbox-etl-runner:latest'
SPARK_DOCKER_NETWORK = 'dev-sandbox'
SPARK_SUBMIT_CMD = 'spark-submit --master local[*]'

# Tempo máximo de execução das tasks
TASK_EXECUTION_TIMEOUT = timedelta(minutes=10)

# Configuração de execução padrão para DockerOperator
DOCKER_OPERATOR_DEFAULTS = {
    'image': SPARK_IMAGE,
    'api_version': 'auto',
    'auto_remove': 'success',
    'docker_url': 'unix://var/run/docker.sock',
    'network_mode': SPARK_DOCKER_NETWORK,
    'mount_tmp_dir': False,
    'tty': False,
    'execution_timeout': TASK_EXECUTION_TIMEOUT,
}