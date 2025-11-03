import logging
from functools import wraps
from typing import Callable

logger = logging.getLogger("humanLogger")

def human_log(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        text, err = func(*args, **kwargs)
        if err:
            logger.error(text)
        else:
            logger.info(text)
    return wrapper
