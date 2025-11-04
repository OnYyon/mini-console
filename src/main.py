import typer

from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.pwd import pwd
from src.commands.cat import cat
from src.commands.cp import cp

#TODO: make a correct create .env or check exists

app = typer.Typer()

app.command()(ls)
app.command()(cd)
app.command()(pwd)
app.command()(cat)
app.command()(cp)

if __name__ == "__main__":
    app()
