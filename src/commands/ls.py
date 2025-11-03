import sys
import stat
import time
import pathlib

import typer
from rich import print
from typing import Generator
from typer import Argument, Option
from typing_extensions import Annotated

from src.logger.human_logger import human_log


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
def ls(
    ctx: typer.Context,
    path: Annotated[str, Argument(help="path to look dir")] = ".",
    is_long: Annotated[bool, Option("-l", help="List files in the long format")] = False,
    is_all: Annotated[bool, Option("-a",
                                   help="Include directory entries whose names begin with a dot.")] = False,
) -> tuple[str, bool]:
    full_cmd = " ".join(sys.argv[1:])
    try:
        resolve_path = pathlib.Path(path).expanduser().resolve()
        if not resolve_path.exists():
            print(f"ls: {resolve_path}: [red]No such file or directory[/red]")
            return f"No such file or directory: {resolve_path}", False

        if resolve_path.is_file():
            print(resolve_path.name)
            return full_cmd, True

        items = ((item, item.name) for item in resolve_path.iterdir())
        if not is_all:
            items = (item for item in items if not item[1].startswith("."))

        if is_long:
            items = get_long_format(items)

        for item in items:
            print(item[1])
        return full_cmd, False
    except PermissionError:
        print(f"ls: {path}: [red]Permission denied[/red]")
        return f"Permission denied: {path}", True
