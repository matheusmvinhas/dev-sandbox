from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import timedelta
from utils.env_loader import get_env_variable

class CustomDockerOperator(DockerOperator):
    def __init__(self, **kwargs):
        default_environment = {
            "SPARK_VERSION": get_env_variable("SPARK_VERSION"),
            "MINIO_ENDPOINT": get_env_variable("MINIO_ENDPOINT"),
            "MINIO_ACCESS_KEY": get_env_variable("MINIO_ACCESS_KEY"),
            "MINIO_SECRET_KEY": get_env_variable("MINIO_SECRET_KEY"),
            "AWS_ACCESS_KEY_ID": get_env_variable("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": get_env_variable("AWS_SECRET_ACCESS_KEY"),
        }

        mounts = [
            Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/scripts", target="/app/scripts", type="bind"),
            Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/utils", target="/app/utils", type="bind"),
            Mount(source="/Users/matheusvinhas/projects/dev-sandbox/minIo/staging/spark-events", target="/tmp/spark-events", type="bind"),
            Mount(source="/Users/matheusvinhas/projects/dev-sandbox/dataplataform/spark-jars", target="/app/spark-jars", type="bind")
        ]

        kwargs.setdefault('image', 'dev-sandbox-etl-runner:latest')
        kwargs.setdefault('api_version', 'auto')
        kwargs.setdefault('auto_remove', 'success')
        kwargs.setdefault('docker_url', 'unix://var/run/docker.sock')
        kwargs.setdefault('network_mode', 'orchestration_dev-sandbox')
        kwargs.setdefault('environment', default_environment)
        kwargs.setdefault('mounts', mounts)
        kwargs.setdefault('tty', False)
        kwargs.setdefault('mount_tmp_dir', False)
        kwargs.setdefault('execution_timeout', timedelta(minutes=10))

        super().__init__(**kwargs)