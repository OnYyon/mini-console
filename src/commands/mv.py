import typer
import shutil
from rich import print
from typing_extensions import Annotated

from src.logger.json_logger import json_log
from src.logger.human_logger import human_log
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history


@human_log
@json_log
@make_history
def mv(
        ctx: typer.Context,
        source: Annotated[str, typer.Argument()],
        target: Annotated[str, typer.Argument()],
):
    source_path = make_abs_path(source, False)
    target_path = make_abs_path(target, True, source_path.name)

    ctx.data = {"command": ctx.info_name, "source": str(source_path), "target": str(target_path)} # type: ignore

    if not source_path.exists():
        print(f"mv: {source_path}: [red]No such file or directory[/red]")
        raise FileNotFoundError("No such file or directory")

    try:
        shutil.move(str(source_path), str(target_path))
        print(f"Moved [purple]{source_path}[/purple] to [purple]{target_path}[/purple]")
    except PermissionError:
        print("mv: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
