from dotenv import load_dotenv
import os

load_dotenv()  # carrega variáveis do .env para os os.environ

def get_env_variable(key: str, default: str = None) -> str:
    return os.getenv(key, default)