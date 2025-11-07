import dotenv
import typer
import pathlib
from rich import print
from typer import Argument
from typing import Optional
from typing_extensions import Annotated

from src.constants import ENV_PATH
from src.logger.human_logger import human_log
from src.utils.history_decorator import make_history


#TODO: simple is more important
@human_log
@make_history
def cd(
    ctx: typer.Context,
    path: Annotated[Optional[str], Argument(help="change dir to")] = None
):
    """Меняет переменную окружения PYTHON_CONSOLE_PATH"""
    if not path:
        t = str(pathlib.Path("~").expanduser().resolve())
        dotenv.set_key(ENV_PATH, "PYTHON_CONSOLE_PATH", t)
        print(f"dir changed to {t}")
        return

    if pathlib.Path(path).is_absolute():
        t = str(pathlib.Path(path).expanduser().resolve())
        dotenv.set_key(ENV_PATH, "PYTHON_CONSOLE_PATH", t)
        print(f"dir changed to {t}")
        return

    try:
        cur_path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not cur_path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")

        resolve_path = (pathlib.Path(cur_path).expanduser().resolve() / path).resolve()
        if not resolve_path.exists():
            print(f"cd: [red]no such file or directory[/red]: [violet]{ctx.params['path']}[/violet]")
            raise FileNotFoundError("no such file or directory")

        if resolve_path.is_file():
            print(f"cd: [red]not a directory[/red]: [violet]{ctx.params['path']}[/violet]")
            raise NotADirectoryError("not a directory")

        dotenv.set_key(ENV_PATH, "PYTHON_CONSOLE_PATH", str(resolve_path))
        print(f"dir changed to {resolve_path}")
    except PermissionError:
        print(f"cd: [red]Permission denied[/red]: [violet]{ctx.params['path']}[/violet]")
        raise PermissionError(f"Permission denied: {ctx.params['path']}")
