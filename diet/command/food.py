import click

from crud.repo import FoodYamlRepo
from crud.models import Protein, Vegs, Carbs
from crud.models import FoodTypeEnum
from component.pprint import print_food_list


@click.group()
@click.pass_context
def food(ctx):
    ctx.obj["food_repo"] = FoodYamlRepo(ctx.obj["data_folder_path"])


@click.command()
@click.option("--name", prompt="Food name")
@click.option("--ftype",
              prompt="Food type",
              type=click.Choice(FoodTypeEnum.__members__.values(),
                                case_sensitive=False))
@click.option("--carb", prompt="Carbs per gram")
@click.option("--fat", prompt="Fat per gram")
@click.option("--protein", prompt="Protein per gram")
@click.option("--calories", prompt="Calories per gram")
@click.pass_context
def add(ctx, name, ftype, carb, fat, protein, calories):
    match ftype:
        case FoodTypeEnum.PROTEIN:
            food_class = Protein
        case FoodTypeEnum.CARBS:
            food_class = Carbs
        case FoodTypeEnum.VEGS:
            food_class = Vegs
        case _:
            raise ValueError("Invalid food type")
    ctx.obj["food_repo"].add([
        food_class(
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
    print_food_list(ctx.obj["food_repo"].get_all())


@click.command()
@click.option("--name", prompt="Food name to update")
@click.option("--ftype",
              prompt="New food type",
              type=click.Choice(FoodTypeEnum.__members__.values(),
                                case_sensitive=False))
@click.option("--carb", prompt="New carbs per gram")
@click.option("--fat", prompt="New fat per gram")
@click.option("--protein", prompt="New protein per gram")
@click.option("--calories", prompt="New calories per gram")
@click.pass_context
def update(ctx, name, ftype, carb, fat, protein, calories):
    match ftype:
        case FoodTypeEnum.PROTEIN:
            food_class = Protein
        case FoodTypeEnum.CARBS:
            food_class = Carbs
        case FoodTypeEnum.VEGS:
            food_class = Vegs
        case _:
            raise ValueError("Invalid food type")
    ctx.obj["food_repo"].modify(
        food_class(
            name=name,
            protein_percentage=protein,
            carbohydrate_percentage=carb,
            fat_percentage=fat,
            calories_per_g=calories,
        ))


@click.command()
@click.option("--name", prompt="Food name to delete")
@click.pass_context
def delete(ctx, name):
    ctx.obj["food_repo"].delete(name)


food.add_command(add, "add")
food.add_command(list_, "list")
food.add_command(update, "update")
food.add_command(delete, "delete")
