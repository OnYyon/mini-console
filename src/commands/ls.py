import stat
import time
import typer
import dotenv
import pathlib
from rich import print
from typing import Optional
from typing import Generator
from typer import Argument, Option
from typing_extensions import Annotated

from src.constants import ENV_PATH
from src.logger.human_logger import human_log
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history


def get_long_format(
        items: Generator[tuple[pathlib.Path, str], None, None]
) -> Generator[tuple[pathlib.Path, str], None, None]:
    month_in_sec = 15552000
    for item in items:
        mode = stat.filemode(item[0].stat().st_mode)
        cnt_sym_link = item[0].stat().st_nlink
        owner = item[0].owner()
        group = item[0].group()
        size = item[0].stat().st_size
        sec = item[0].stat().st_mtime
        now = time.time()
        if now - sec < month_in_sec:
            last_touch = time.strftime("%d %b %H:%M", time.localtime(sec))
        else:
            last_touch = time.strftime("%d %b  %Y", time.localtime(sec))
        yield item[0], f"{mode} {cnt_sym_link:>2} {owner}  {group} {size:>8} {last_touch} {item[1]}"

#TODO: Mark a dir
@human_log
@make_history
def ls(
    ctx: typer.Context,
    path: Annotated[Optional[str], Argument(help="path to look dir")] = None,
    is_long: Annotated[bool, Option("-l", help="List files in the long format")] = False,
    is_all: Annotated[bool, Option("-a",
                                   help="Include directory entries whose names begin with a dot.")] = False,
):
    if not path:
        path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")

    try:
        resolve_path = make_abs_path(path, False)
        print(resolve_path)
        if not resolve_path.exists():
            print(f"ls: {ctx.params['path']}: [red]No such file or directory[/red]")
            raise FileNotFoundError("No such file or directory")

        if resolve_path.is_file():
            print(ctx.params["path"])
            return

        items = ((item, item.name) for item in resolve_path.iterdir())
        if not is_all:
            items = (item for item in items if not item[1].startswith("."))

        if is_long:
            items = get_long_format(items)

        for item in items:
            print(item[1])

    except PermissionError:
        print(f"ls: {path}: [red]Permission denied[/red]")
        raise PermissionError(f"Permission denied: {path}")
