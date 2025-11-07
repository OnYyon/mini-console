import logging
import sys
import typer
import structlog
from functools import wraps
from typing import Callable

log_file = open("./src/logs/undo_commands.json.log", "a", encoding="utf-8")

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.WriteLoggerFactory(file=log_file),
    cache_logger_on_first_use=True,
)

json_logger = structlog.get_logger()
logger = logging.getLogger("json")

def json_log(func: Callable):
    """декоратор для логов в машином представляние для обрабтки при undo"""
    @wraps(func)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        cmd = " ".join(sys.argv[1:])
        try:
            func(ctx, *args, **kwargs)
            data = []
            if hasattr(ctx, "data"):
                data = ctx.data
            json_logger.info(
                f"execute: {ctx.command.name}",
                command=cmd,
                function=ctx.command.name,
                params=ctx.params,
                paths=data,
            )
        except Exception:
            raise
    return wrapper
