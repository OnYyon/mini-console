import typer
import dotenv
import pathlib
import shutil
from rich import print
from typing_extensions import Annotated

from src.logger.json_logger import json_log
from src.logger.human_logger import human_log
from src.constants import ENV_PATH, TRASH_PATH
from src.utils.history_decorator import make_history


def generate_unique_name(trash_path: pathlib.Path, original_name: str) -> str:
    base_name = original_name
    counter = 1

    while (trash_path / base_name).exists():
        name_parts = original_name.split('.')
        if len(name_parts) > 1:
            base_name = f"{'.'.join(name_parts[:-1])}_{counter}.{name_parts[-1]}"
        else:
            base_name = f"{original_name}_{counter}"
        counter += 1

    return base_name

# TODO: check trash dir else create
@human_log
@json_log
@make_history
def rm(
        ctx: typer.Context,
        target: Annotated[str, typer.Argument()],
        recursive: Annotated[bool, typer.Option()] = False,
):
    trash_path = pathlib.Path(TRASH_PATH).expanduser().resolve()

    target_path = pathlib.Path(target)
    if not target_path.is_absolute():
        cur_path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not cur_path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")
        target_path = pathlib.Path(cur_path) / target_path
    target_path = target_path.expanduser().resolve()

    try:
        if not target_path.exists():
            print(f"rm: {ctx.params['target']}: No such file or directory")
            raise FileNotFoundError("No such file or directory")

        if target_path.is_dir():
            if not recursive:
                print(f"rm: {ctx.params['target']}: is a directory (use -r to remove recursively)")
                raise IsADirectoryError("Cannot remove directory without -r")

            unique_name = generate_unique_name(trash_path, target_path.name)
            trash_target = trash_path / unique_name

            shutil.move(str(target_path), str(trash_target))
        else:
            unique_name = generate_unique_name(trash_path, target_path.name)
            trash_target = trash_path / unique_name

            shutil.move(str(target_path), str(trash_target))
        print(f"Delete [purple]{trash_path}[/purple] to [purple]trash[/purple]")

    except PermissionError:
        print(f"rm: {target}: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
