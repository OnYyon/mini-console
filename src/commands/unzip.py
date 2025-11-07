import typer
from rich import print
from zipfile import ZipFile
from typing_extensions import Annotated

from src.logger.human_logger import human_log
from src.utils.get_from_env import get_from_env
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history
from src.utils.generate_unique_name import generate_unique_name


@human_log
@make_history
def unzip(
    ctx: typer.Context,
    path: Annotated[str, typer.Argument(help="path to archive.zip")],
):
    source_path = make_abs_path(path, False)
    cur_path = make_abs_path(get_from_env("PYTHON_CONSOLE_PATH"), False)

    if not source_path.exists():
        print(f"mv: {source_path}: [red]No such file or directory[/red]")
        raise FileNotFoundError("No such file or directory")

    t = (cur_path / source_path.name.rstrip(".zip")).expanduser().resolve()
    if t.exists():
        unique_name = generate_unique_name(cur_path, source_path.name.rstrip(".zip"))
        t = (cur_path / unique_name).expanduser().resolve()
        t.mkdir(exist_ok=False)
    else:
        t.mkdir(exist_ok=False)

    try:
        with ZipFile(source_path) as zip:
            zip.extractall(cur_path)
        print(f"unzip: extract to {cur_path} with name [purple]{t.name}[/purple]")
    except PermissionError:
        print("unzip: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
