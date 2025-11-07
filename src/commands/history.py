import typer
from rich import print
from collections import deque
from typing_extensions import Annotated

from src.constants import HISTORY_PATH
from src.logger.human_logger import human_log
from src.utils.history_decorator import make_history


@human_log
@make_history
def history(
    ctx: typer.Context,
    lines: Annotated[int, typer.Argument(help="How many lines")] = 10,
):
    """Возвращяем историю из файда .history"""
    if lines < 0:
        print("history: [red]negative number of rows[/red]")
        raise ValueError("negative number of rows")

    with open(HISTORY_PATH, encoding="utf-8") as f:
        for line in deque(f, lines):
            print(line, end="")
