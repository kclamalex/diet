import click
from command.food import food


@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj["data_folder_path"] = "./data"

cli.add_command(food)

