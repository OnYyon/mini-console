import typer
from pathlib import Path
from dotenv import set_key


def build_environment():
    """Создает нужные папки при необходимости."""
    env_path = Path("./.env")
    logs_dir = Path("./src/logs")
    history_dir = Path("./src/history")
    trash_dir = Path("./src/.trash")

    if not env_path.exists():
        env_path.write_text("")
        set_key(str(env_path), "PYTHON_CONSOLE_PATH", "~")
        set_key(str(env_path), "HISTORY_COUNT", "0")

    logs_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)
    trash_dir.mkdir(parents=True, exist_ok=True)

def main():
    build_environment()

    app = typer.Typer()

    from src.commands.ls import ls
    from src.commands.cd import cd
    from src.commands.pwd import pwd
    from src.commands.cat import cat
    from src.commands.cp import cp
    from src.commands.mv import mv
    from src.commands.rm import rm
    from src.commands.history import history
    from src.commands.zip import zip
    from src.commands.unzip import unzip
    from src.commands.tar import tar
    from src.commands.untar import untar
    from src.commands.undo import undo
    from src.commands.grep import grep

    app.command()(ls)
    app.command()(cd)
    app.command()(pwd)
    app.command()(cat)
    app.command()(cp)
    app.command()(mv)
    app.command()(rm)
    app.command()(history)
    app.command()(zip)
    app.command()(unzip)
    app.command()(tar)
    app.command()(untar)
    app.command()(undo)
    app.command()(grep)

    app()


if __name__ == "__main__":
    main()
