import typer
import tarfile
from rich import print
from tarfile import ReadError
from typing_extensions import Annotated

from src.logger.human_logger import human_log
from src.utils.get_from_env import get_from_env
from src.utils.make_abs_path import make_abs_path
from src.utils.history_decorator import make_history
from src.utils.generate_unique_name import generate_unique_name


@human_log
@make_history
def untar(
        ctx: typer.Context,
        path: Annotated[str, typer.Argument(help="path to archive.tar")],
):
    source_path = make_abs_path(path, False)
    cur_path = make_abs_path(get_from_env("PYTHON_CONSOLE_PATH"), False)

    if not source_path.exists():
        print("untar: {source_path}: [red]No such file or directory[/red]")
        raise FileNotFoundError("No such file or directory")

    archive_name = source_path.name

    if archive_name.endswith('.tar.gz'):
        folder_name = archive_name[:-7]
    elif archive_name.endswith('.tgz'):
        folder_name = archive_name[:-4]
    elif archive_name.endswith('.tar'):
        folder_name = archive_name[:-4]
    else:
        folder_name = archive_name

    t = (cur_path / folder_name).expanduser().resolve()

    if t.exists():
        unique_name = generate_unique_name(cur_path, folder_name)
        t = (cur_path / unique_name).expanduser().resolve()
        t.mkdir(exist_ok=False)
    else:
        t.mkdir(exist_ok=False)

    try:
        with tarfile.open(source_path, "r:*") as tar:
            tar.extractall(path=t)

        print(f"untar: extracted to {t.parent} with name [purple]{t.name}[/purple]")
    except tarfile.ReadError:
        print("untar: [red]Cannot read tar archive or unsupported format[/red]")
        raise ReadError("Cannot read tar archive or unsupported")
    except PermissionError:
        print("untar: [red]Permission denied[/red]")
        raise PermissionError("Permission denied")
