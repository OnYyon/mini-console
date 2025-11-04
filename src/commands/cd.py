import dotenv
import typer
import pathlib
from rich import print
from typer import Argument
from typing_extensions import Annotated

from src.constants import ENV_PATH
from src.logger.human_logger import human_log
from src.utils.history_decorator import make_history


@human_log
@make_history
def cd(
    ctx: typer.Context,
    path: Annotated[str, Argument()] | None = None
):
    if not path:
        dotenv.set_key(ENV_PATH, "PYTHON_CONSOLE_PATH", "~")
        print("dir changed to ~")
        return

    try:
        path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")
        cur_path = pathlib.Path(path).expanduser().resolve()

        resolve_path = cur_path / path
        if not resolve_path.exists():
            print(f"cd: [red]no such file or directory[/red]: [violet]{ctx.params['path']}[/violet]")
            print(resolve_path)
            raise FileNotFoundError("no such file or directory")

        if resolve_path.is_file():
            print(f"cd: [red]not a directory[/red]: [violet]{ctx.params['path']}[/violet]")
            raise NotADirectoryError("not a directory")
        dotenv.set_key(ENV_PATH, "PYTHON_CONSOLE_PATH", str(resolve_path))
        print(f"dir changed to {resolve_path}")
    except PermissionError:
        print(f"cd: [red]Permission denied[/red]: [violet]{ctx.params['path']}[/violet]")
        raise PermissionError(f"Permission denied: {ctx.params['path']}")
