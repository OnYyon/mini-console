from typer import Argument
from typing_extensions import Annotated


def cd(
    path: Annotated[str, Argument()] = "."
):
    ...
