import typer

from src.commands.ls import ls
from src.commands.cd import cd


app = typer.Typer()

app.command()(ls)
app.command()(cd)

if __name__ == "__main__":
    app()
