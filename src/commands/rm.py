import typer
import pathlib
import shutil
from rich import print
from typing_extensions import Annotated

from src.constants import TRASH_PATH
from src.logger.json_logger import json_log
from src.logger.human_logger import human_log
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history
from src.utils.generate_unique_name import generate_unique_name


# TODO: check trash dir else create
@human_log
@json_log
@make_history
def rm(
        ctx: typer.Context,
        target: Annotated[str, typer.Argument()],
        recursive: Annotated[bool, typer.Option("-r")] = False,
):
    trash_path = pathlib.Path(TRASH_PATH).expanduser().resolve()

    target_path = make_abs_path(target, False)

    ctx.data = {"command": ctx.info_name, "source": str(target_path), "target": str(trash_path / target_path.name)} # type: ignore

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
        print(f"Delete [purple]{target_path}[/purple] to [purple]trash[/purple]")

    except PermissionError:
        print(f"rm: {target}: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
