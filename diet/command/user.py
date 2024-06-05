import click

from crud.repo import ConsumptionYamlRepo
from crud.models import Consumption


@click.group()
@click.pass_context
def user(ctx):
    ctx.obj["user_repo"] = ConsumptionYamlRepo(ctx.obj["data_folder_path"])


@click.command()
@click.option("--name", prompt="User name:")
@click.option("--carb", prompt="Carbs consumption gram per day:")
@click.option("--fat", prompt="Fat consumption gram per day:")
@click.option("--protein", prompt="Protein pconsumption gram per day:")
@click.pass_context
def add(ctx, name, carb, fat, protein):
    ctx.obj["user_repo"].add(
        [Consumption(name=name,
             protein_percentage=protein,
             carbohydrate_percentage=carb,
             fat_percentage=fat)])

user.add_command(add, "add")
