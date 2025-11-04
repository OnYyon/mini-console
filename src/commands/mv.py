import typer
import dotenv
import pathlib
import shutil
from rich import print
from typing_extensions import Annotated

from src.constants import ENV_PATH
from src.logger.json_logger import json_log
from src.logger.human_logger import human_log
from src.utils.history_decorator import make_history


@human_log
@json_log
@make_history
def mv(
        ctx: typer.Context,
        source: Annotated[str, typer.Argument()],
        target: Annotated[str, typer.Argument()],
):
    source_path = pathlib.Path(source)
    if not source_path.is_absolute():
        cur_path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not cur_path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")
        source_path = pathlib.Path(cur_path) / source_path
    source_path = source_path.expanduser().resolve()

    target_path = pathlib.Path(target)
    if not target_path.is_absolute():
        cur_path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not cur_path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")

        target_path = pathlib.Path(cur_path) / target_path
        if target_path.exists() and target_path.is_dir():
            target_path = target_path / source_path.name

    target_path = target_path.expanduser().resolve()

    try:
        if not source_path.exists():
            print(f"mv: {source_path}: [red]No such file or directory[/red]")
            raise FileNotFoundError("No such file or directory")

        if target_path.exists() and target_path.is_dir():
            final_target = target_path / source_path.name
        else:
            final_target = target_path

        shutil.move(str(source_path), str(final_target))
        print(f"Moved [purple]{source_path}[/purple] to [purple]{final_target}[/purple]")

    except PermissionError:
        print("mv: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
