from typing import Literal

import typer
import tarfile
from rich import print
from typing_extensions import Annotated

from src.logger.human_logger import human_log
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history


@human_log
@make_history
def tar(
    ctx: typer.Context,
    source: Annotated[str, typer.Argument(help="Archive name")],
    target: Annotated[str, typer.Argument(help="Folder to zip")],
    compress: Annotated[bool, typer.Option("-z", help="Use gzip compression")] = False,
):
    """создает tar архив из дириктории. Есть возможность с сжимаиние флаг compress"""
    source_path = make_abs_path(source, False)
    target_path = make_abs_path(target, False)

    if compress:
        if source_path.suffix.lower() not in ['.tar.gz', '.tgz']:
            source_path = source_path.with_suffix('.tar.gz')
    else:
        if source_path.suffix.lower() != '.tar':
            source_path = source_path.with_suffix('.tar')

    try:
        if not target_path.exists():
            print(f"zip: {target}: No such file or directory")
            raise FileNotFoundError("No such file or directory")

        if not target_path.is_dir():
            print(f"zip: {target}: Is not a directory")
            raise NotADirectoryError("Is not a directory")

        md: Literal["w", "w:gz"] = "w:gz" if compress else "w"

        with tarfile.open(str(source_path), md) as tar:
            for file_path in target_path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(target_path.parent)
                    tar.add(file_path, arcname)
                    print(f"adding: [purple]{arcname}[/purple]")

        print(f"Created archive {'compressed' if compress else ''}: [purple]{source_path}[/purple]")
    except PermissionError:
        print("tar: Permission denied")
        raise PermissionError("Permission denied")
