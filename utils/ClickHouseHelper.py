import os
from dotenv import load_dotenv
from clickhouse_connect import get_client

load_dotenv()  # Carrega variáveis do .env

def get_clickhouse_client():
    """
    Retorna uma instância do client ClickHouse usando variáveis do .env
    """
    return get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_HTTP_PORT", 8123)),
        database=os.getenv("CLICKHOUSE_DATABASE"),
        username=os.getenv("CLICKHOUSE_USER"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "")
    )