import click

from diet.command import food, plan, shop, user


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj["data_folder_path"] = "./data"


cli.add_command(food)
cli.add_command(user)
cli.add_command(plan)
cli.add_command(shop)
