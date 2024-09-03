from uuid import uuid4

import click
from tabulate import tabulate

from diet.crud import models
from diet.crud.models import Carbs, FoodTypeEnum, Protein, Vegs
from diet.crud.repo import FoodYamlRepo
from diet.utils import str_to_snake_case


@click.group()
@click.pass_context
def food(ctx):
    pass


@click.command()
@click.option("--name", prompt="Food name")
@click.option(
    "--ftype",
    prompt="Food type",
    type=click.Choice(FoodTypeEnum.__members__.values(), case_sensitive=False),
)
@click.option("--carb", prompt="Carbs per gram")
@click.option("--fat", prompt="Fat per gram")
@click.option("--protein", prompt="Protein per gram")
@click.option("--calories", prompt="Calories per gram")
@click.pass_context
def add(ctx, name, ftype, carb, fat, protein, calories):
    food_repo = FoodYamlRepo(ctx.obj["data_folder_path"])
    name = str_to_snake_case(name)
    match ftype:
        case FoodTypeEnum.PROTEIN:
            food_class = Protein
        case FoodTypeEnum.CARBS:
            food_class = Carbs
        case FoodTypeEnum.VEGS:
            food_class = Vegs
        case _:
            raise ValueError("Invalid food type")
    food_repo.add(
        food_class(
            id=str(uuid4()),
            name=name,
            protein_per_gram=protein,
            carbs_per_gram=carb,
            fat_per_gram=fat,
            calories_per_gram=calories,
        )
    )


@click.command()
@click.pass_context
def list_(ctx):
    food_repo = FoodYamlRepo(ctx.obj["data_folder_path"])
    food_list: list[models.Food] = food_repo.get_all()
    table = []
    headers = [
        "name",
        "type",
        "protein per gram",
        "carbs per gram",
        "fat per gram",
        "calories per gram",
    ]

    for f in food_list:
        table.append(
            [
                f.name,
                f.food_type,
                f.protein_per_gram,
                f.carbs_per_gram,
                f.fat_per_gram,
                f.calories_per_gram,
            ]
        )
    print(tabulate(table, headers=headers))


@click.command()
@click.option("--name", prompt="Food name to update")
@click.option(
    "--ftype",
    prompt="New food type",
    type=click.Choice(FoodTypeEnum.__members__.values(), case_sensitive=False),
)
@click.option("--carb", prompt="New carbs per gram")
@click.option("--fat", prompt="New fat per gram")
@click.option("--protein", prompt="New protein per gram")
@click.option("--calories", prompt="New calories per gram")
@click.pass_context
def update(ctx, name, ftype, carb, fat, protein, calories):
    food_repo = FoodYamlRepo(ctx.obj["data_folder_path"])
    match ftype:
        case FoodTypeEnum.PROTEIN:
            food_class = Protein
        case FoodTypeEnum.CARBS:
            food_class = Carbs
        case FoodTypeEnum.VEGS:
            food_class = Vegs
        case _:
            raise ValueError("Invalid food type")
    food_repo.modify(
        food_class(
            name=name,
            protein_per_gram=protein,
            carbs_per_gram=carb,
            fat_per_gram=fat,
            calories_per_gram=calories,
        )
    )


@click.command()
@click.option("--name", prompt="Food name to delete")
@click.pass_context
def delete(ctx, name):
    food_repo = FoodYamlRepo(ctx.obj["data_folder_path"])
    food_repo.delete(name)


food.add_command(add, "add")
food.add_command(list_, "list")
food.add_command(update, "update")
food.add_command(delete, "delete")
