import sys
import dotenv
from typer import Context
from functools import wraps
from typing import Callable
from src.constants import HISTORY_PATH, ENV_PATH


def make_history(func: Callable):
    @wraps(func)
    def wrapper(ctx: Context, *args, **kwargs):
        try:
            t = dotenv.get_key(ENV_PATH, "HISTORY_COUNT")
            if not t:
                raise FileNotFoundError("Dont have .env")

            cnt = int(t)
            cnt += 1
            dotenv.set_key(ENV_PATH, "HISTORY_COUNT", str(cnt))
            with open(HISTORY_PATH, "a") as f:
                f.write(f"{cnt:<} {' '.join(sys.argv[1:])}\n")
            func(ctx, *args, **kwargs)
        except Exception:
            raise
    return wrapper
