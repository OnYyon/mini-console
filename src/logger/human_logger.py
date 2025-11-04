import sys
import typer
import logging
from functools import wraps
from typing import Callable


logger = logging.getLogger("humanLogger")

def human_log(func: Callable):
    @wraps(func)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        try:
            func(ctx, *args, **kwargs)
            logger.info(" ".join(sys.argv[1:]))
        except (FileNotFoundError, PermissionError) as e:
            logging.error(e)
        except Exception as e:
            logging.critical(e)
    return wrapper
