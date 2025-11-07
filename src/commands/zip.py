import typer
import zipfile
from rich import print
from typing_extensions import Annotated

from src.logger.human_logger import human_log
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history


@human_log
@make_history
def zip(
        ctx: typer.Context,
        source: Annotated[str, typer.Argument(help="Archive name")],
        target: Annotated[str, typer.Argument(help="Folder to zip")],
):
    """Создает zip архив из папки только"""
    source_path = make_abs_path(source, False)

    target_path = make_abs_path(target, False)
    if source_path.suffix.lower() != '.zip':
        source_path = source_path.with_suffix('.zip')

    try:
        if not target_path.exists():
            print(f"zip: {target}: No such file or directory")
            raise FileNotFoundError("No such file or directory")

        if not target_path.is_dir():
            print(f"zip: {target}: Is not a directory")
            raise NotADirectoryError("Is not a directory")

        with zipfile.ZipFile(source_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in target_path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(target_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"adding: [purple]{arcname}[/purple]")

        print(f"Created archive: [purple]{source_path}[/purple]")

    except PermissionError:
        print("zip: Permission denied")
        raise PermissionError("Permission denied")
