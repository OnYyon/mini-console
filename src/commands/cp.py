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
def cp(
        ctx: typer.Context,
        source: Annotated[str, typer.Argument()],
        target: Annotated[str, typer.Argument()],
        recursive: Annotated[bool, typer.Option("-r", "-R")] = False,
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

        temp_target = pathlib.Path(cur_path) / target_path
        if temp_target.exists() and temp_target.is_dir():
            target_path = temp_target / source_path.name
    target_path = target_path.expanduser().resolve()

    try:
        if not source_path.exists():
            print(f"cp: [purple]{source}[/purple]: [red]No such file or directory[/red]")
            raise FileNotFoundError("No such file or directory")

        if recursive:
            if source_path.is_dir():
                shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                print(f"Copied directory [purple]{source}[/purple] to [purple]{target}[/purple]")
            else:
                print(f"cp: -r not specified; omitting directory [purple]{source}[/purple]")
                raise ValueError("Cannot copy directory without -r flag")

        else:
            if source_path.is_file():
                shutil.copy2(source_path, target_path)
                print(f"Copied [purple]{source}[/purple] to [purple]{target}[/purple]")
            elif source_path.is_dir():
                print(f"cp: -r not specified; omitting directory [purple]{source}[/purple]")
                raise ValueError("Cannot copy directory without -r flag")

    except FileExistsError:
        print(f"cp: cannot overwrite directory [purple]{target}[/purple] with non-directory")
        raise FileExistsError("File exists ")
    except PermissionError:
        print("cp: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
