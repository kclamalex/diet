import click

from crud.repo import FoodYamlRepo
from crud.models import Food


@click.group()
@click.pass_context
def food(ctx):
    ctx.obj["food_repo"] = FoodYamlRepo(ctx.obj["data_folder_path"])


@click.command()
@click.option("--name", prompt="Food name:")
@click.option("--carb", prompt="Carbs percentage:")
@click.option("--fat", prompt="Fat percentage:")
@click.option("--protein", prompt="Protein percentage:")
@click.option("--ftype",
              prompt="protein or carbonhydrate",
              type=click.Choice(['protein', 'carbonhydrate']))
@click.pass_context
def add(ctx, name, carb, fat, protein, ftype):
    ctx.obj["food_repo"].add(
        [Food(name=name,
             protein_percentage=protein,
             carbohydrate_percentage=carb,
             fat_percentage=fat,
             food_type=ftype)])

food.add_command(add, "add")
