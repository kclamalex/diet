import click

from crud.repo import ConsumptionYamlRepo
from crud.models import Consumption


@click.group()
@click.pass_context
def user(ctx):
    ctx.obj["user_repo"] = ConsumptionYamlRepo(ctx.obj["data_folder_path"])


@click.command()
@click.option("--name", prompt="User name")
@click.option("--carb", prompt="Carbs consumption gram per day")
@click.option("--fat", prompt="Fat consumption gram per day")
@click.option("--protein", prompt="Protein consumption gram per day")
@click.option("--calories", prompt="Calories consumption gram per day")
@click.pass_context
def add(ctx, name, carb, fat, protein, calories):
    ctx.obj["user_repo"].add([
        Consumption(
            name=name,
            protein_percentage=protein,
            carbohydrate_percentage=carb,
            fat_percentage=fat,
            calories_per_g=calories,
        )
    ])


@click.command()
@click.pass_context
def list_(ctx):
    print(ctx.obj["user_repo"].get_all())


@click.command()
@click.option("--name", prompt="User name to update")
@click.option("--carb", prompt="Carbs consumption gram per day")
@click.option("--fat", prompt="Fat consumption gram per day")
@click.option("--protein", prompt="Protein consumption gram per day")
@click.option("--calories", prompt="Calories consumption gram per day")
@click.pass_context
def update(ctx, name, carb, fat, protein, calories):
    ctx.obj["user_repo"].update([
        Consumption(
            name=name,
            protein_percentage=protein,
            carbohydrate_percentage=carb,
            fat_percentage=fat,
            calories_per_g=calories,
        )
    ])


@click.command()
@click.option("--name", prompt="User name to delete")
@click.pass_context
def delete(ctx, name):
    ctx.obj["user_repo"].delete(name)


user.add_command(add, "add")
user.add_command(list_, "list")
user.add_command(update, "update")
user.add_command(delete, "delete")
