import typer

from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.pwd import pwd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm
from src.commands.history import history
from src.commands.zip import zip
from src.commands.unzip import  unzip
from src.commands.tar import tar
from src.commands.untar import untar
from src.commands.undo import undo

# TODO: make a correct create .env or check exists

# TODO: Make clean architecture with max scaling and productive

app = typer.Typer()

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

if __name__ == "__main__":
    app()
