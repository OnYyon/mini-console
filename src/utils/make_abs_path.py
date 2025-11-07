import pathlib
from src.utils.get_from_env import get_from_env


# TODO: Check errors
def make_abs_path(path: str, add_dir: bool, dir_name: str | None = None) -> pathlib.Path:
    """делаем абсолютный путь """
    abs_path = pathlib.Path(path).expanduser()
    if not abs_path.is_absolute():
        cur_path = get_from_env("PYTHON_CONSOLE_PATH")
        abs_path = pathlib.Path(cur_path) / abs_path

    abs_path = abs_path.resolve()

    if add_dir:
        if not dir_name:
            raise ValueError("add_dir requires dir_name")
        if abs_path.exists() and abs_path.is_dir():
            abs_path = abs_path / dir_name

    return abs_path
