import typer
import dotenv
import pathlib
from rich import print

from src.constants import ENV_PATH
from src.logger.human_logger import human_log
from src.utils.history_decorator import make_history

@human_log
@make_history
def pwd(ctx: typer.Context):
    path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
    if not path:
        print("Dont have .env")
        raise FileNotFoundError("Dont have .env")
    print(pathlib.Path(path).expanduser().resolve())
