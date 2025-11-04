import typer

from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.pwd import pwd

#TODO: make a correct create .env or check exists

app = typer.Typer()

app.command()(ls)
app.command()(cd)
app.command()(pwd)

if __name__ == "__main__":
    app()
