import typer
import dotenv
import pathlib
from rich import print
from typing_extensions import Annotated

from src.constants import ENV_PATH
from src.logger.human_logger import human_log
from src.utils.history_decorator import make_history


@human_log
@make_history
def cat(
        ctx: typer.Context,
        path: Annotated[str, typer.Argument(help="path to file")]
):
    if pathlib.Path(path).is_absolute():
        with open(pathlib.Path(path).expanduser().resolve(), encoding="utf-8") as f:
            while line := f.readline():
                print(line, end="")
        return

    try:
        cur_path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not cur_path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")

        resolve_path = (pathlib.Path(cur_path).expanduser().resolve() / path).resolve()

        if resolve_path.is_dir():
            print(f"cat: {ctx.params['path']}: Is a directory")
            raise IsADirectoryError("Is a directory")

        if not resolve_path.exists():
            print(f"cat: {ctx.params['path']}: No such file or directory")
            raise FileNotFoundError("No such file or directory")

        with open(resolve_path, encoding="utf-8") as f:
            while line := f.readline():
                print(line, end="")

    except PermissionError:
        print(f"cat: {path}: [red]Permission denied[/red]")
        raise PermissionError(f"Permission denied: {path}")
