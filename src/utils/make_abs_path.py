import dotenv
import pathlib

from src.constants import ENV_PATH


def make_abs_path(path: str, add_dir: bool, dir_name: str | None = None) -> pathlib.Path:
    abs_path = pathlib.Path(path).expanduser()
    if not abs_path.is_absolute():
        cur_path = dotenv.get_key(ENV_PATH, "PYTHON_CONSOLE_PATH")
        if not cur_path:
            print("Dont find .env file")
            raise FileNotFoundError("dont have .env")
        abs_path = pathlib.Path(cur_path) / abs_path

    abs_path = abs_path.resolve()

    if add_dir:
        if not dir_name:
            raise ValueError("add_dir requires dir_name")
        if abs_path.exists() and abs_path.is_dir():
            abs_path = abs_path / dir_name

    return abs_path
