import re
import typer
import pathlib
from rich import print
from typer import Argument
from typing_extensions import Annotated

from src.logger.human_logger import human_log
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history


@human_log
@make_history
def grep(
    ctx: typer.Context,
    pattern: Annotated[str, Argument(help="Pattern to search for")],
    path: Annotated[str, Argument(help="File or directory path")],
    recursive: Annotated[bool, typer.Option("-r", help="Recursive search in subdirectories")] = False,
    ignore_case: Annotated[bool, typer.Option("-i", help="Case-insensitive search")] = False,
):
    """
    Поиск по файлом
    """
    target_path = make_abs_path(path, False)

    if not target_path.exists():
        print(f"[red]grep: no such file or directory: {path}[/red]")
        raise FileNotFoundError(f"No such file or directory: {path}")

    import re
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        print(f"[red]grep: invalid pattern: {e}[/red]")
        raise ValueError(f"Invalid regex pattern: {e}")

    if target_path.is_file():
        _search_in_file(target_path, regex, ignore_case)

    elif target_path.is_dir():
        if recursive:
            for file_path in target_path.rglob("*"):
                if file_path.is_file():
                    _search_in_file(file_path, regex, ignore_case)
        else:
            for file_path in target_path.iterdir():
                if file_path.is_file():
                    _search_in_file(file_path, regex, ignore_case)
    else:
        print(f"[red]grep: not a file or directory: {path}[/red]")
        raise ValueError(f"Not a file or directory: {path}")


def _search_in_file(file_path: pathlib.Path, regex: re.Pattern, ignore_case: bool):
    """Поиск по одному файлу."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f, 1):
                match = regex.search(line)
                if match:
                    matched_text = line.strip()
                    print(f"[purple]{file_path}[/purple]:{line_num}:{matched_text}")
    except Exception as e:
        print(f"Warning: could not read {file_path}: {e}")
        raise e
