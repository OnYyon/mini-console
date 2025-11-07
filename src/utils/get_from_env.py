from dotenv import get_key
from src.constants import ENV_PATH


def get_from_env(key: str) -> str:
    """получаем значение из .env"""
    t = get_key(ENV_PATH, key)
    if not t:
        print("Dont find .env file")
        raise FileNotFoundError("dont have .env")
    return t
