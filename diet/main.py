import click
from command.food import food
from command.user import user
from command.diet import plan 

@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj["data_folder_path"] = "./data"

cli.add_command(food)
cli.add_command(plan)
cli.add_command(user)
