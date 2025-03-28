import os
import click

from diet.command import food, plan, shop, user


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    # Create data directory if it doesn't exist
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    
    ctx.obj["db_path"] = os.path.join(data_dir, "diet.db")


cli.add_command(food)
cli.add_command(user)
cli.add_command(plan)
cli.add_command(shop)
