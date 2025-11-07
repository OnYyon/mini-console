import json
import shutil
from pathlib import Path
import typer
from rich import print

from src.logger.human_logger import human_log
from src.constants import LOG_FILE, TRASH_PATH
from src.utils.history_decorator import make_history


@human_log
@make_history
def undo(ctx: typer.Context):
    """
    Отмена одной из команд: mv, cp, rm
    """
    log_file = Path(LOG_FILE)
    if not log_file.exists() or log_file.stat().st_size == 0:
        print("[yellow]No operations to undo.[/yellow]")
        return

    lines = log_file.read_text().splitlines()
    if not lines:
        print("[yellow]Undo history is empty.[/yellow]")
        return

    try:
        last_entry = json.loads(lines[-1])
    except json.JSONDecodeError:
        print("[red]Error: corrupted log entry in undo history.[/red]")
        return

    command = last_entry.get("function")
    if command not in ("cp", "mv", "rm"):
        print(f"[red]Unknown command to undo: {command}[/red]")
        return

    source = Path(last_entry["paths"]["source"])
    target = Path(last_entry["paths"]["target"])

    try:
        if command == "cp":
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            print(f"Undo [purple]cp[/purple]: removed [purple]{target}[/purple]")

        elif command == "mv":
            if not target.exists():
                print(f"[red]Cannot undo mv: file not found — {target}[/red]")
                return
            if source.exists():
                print(f"[red]Cannot undo mv: destination already exists — {source}[/red]")
                return
            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(source))
            print(f"Undo [purple]mv[/purple]: restored [purple]{source}[/purple]")

        elif command == "rm":
            if not target.exists():
                print(f"[red]File not found in trash: {target}[/red]")
                return
            if not str(target).startswith(str(TRASH_PATH)):
                print("[yellow]Warning: file is not in trash, but attempting restore...[/yellow]")
            if source.exists():
                print(f"[red]Cannot restore: file already exists — {source}[/red]")
                return
            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(source))
            print(f"Undo [purple]rm[/purple]: restored [purple]{source}[/purple]")

        log_file.write_text("\n".join(lines[:-1]) + ("\n" if len(lines) > 1 else ""))

    except Exception as e:
        print(f"[red]Error during undo: {e}[/red]")
        raise typer.Exit(code=1)
