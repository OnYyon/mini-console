import sys
import typer
import logging
from functools import wraps
from typing import Callable
from tarfile import ReadError

logger = logging.getLogger("humanLogger")


def human_log(func: Callable):
    @wraps(func)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        try:
            func(ctx, *args, **kwargs)
            logger.info(" ".join(sys.argv[1:]))
        except (FileNotFoundError, PermissionError, IsADirectoryError, FileExistsError, ValueError, ReadError) as e:
            logger.error(sys.argv[1] + " " + str(e))
        except Exception as e:
            logger.critical(e)
    return wrapper
