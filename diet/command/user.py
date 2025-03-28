from uuid import uuid4

import click
from tabulate import tabulate

from diet.crud import models
from diet.crud.repo import UserSqliteRepo
from diet.utils import str_to_snake_case


@click.group()
@click.pass_context
def user(ctx):
    pass


@click.command()
@click.option("--name", prompt="User name")
@click.option("--protein", prompt="Required protein per day")
@click.option("--carb", prompt="Required carbs per day")
@click.option("--fat", prompt="Required fat per day")
@click.option("--calories", prompt="Required calories per day")
@click.pass_context
def add(ctx, name, protein, carb, fat, calories):
    user_repo = UserSqliteRepo(ctx.obj["db_path"])
    name = str_to_snake_case(name)
    user_repo.add(
        models.User(
            id=str(uuid4()),
            name=name,
            required_protein_per_day=protein,
            required_carbs_per_day=carb,
            required_fat_per_day=fat,
            required_calories_per_day=calories,
        )
    )


@click.command()
@click.pass_context
def list_(ctx):
    user_repo = UserSqliteRepo(ctx.obj["db_path"])
    user_list: list[models.User] = user_repo.get_all()
    table = []
    headers = [
        "name",
        "required protein per day",
        "required carbs per day",
        "required fat per day",
        "required calories per day",
    ]

    for u in user_list:
        table.append(
            [
                u.name,
                u.required_protein_per_day,
                u.required_carbs_per_day,
                u.required_fat_per_day,
                u.required_calories_per_day,
            ]
        )
    print(tabulate(table, headers=headers))


@click.command()
@click.option("--name", prompt="User name to update")
@click.option("--protein", prompt="New required protein per day")
@click.option("--carb", prompt="New required carbs per day")
@click.option("--fat", prompt="New required fat per day")
@click.option("--calories", prompt="New required calories per day")
@click.pass_context
def update(ctx, name, protein, carb, fat, calories):
    user_repo = UserSqliteRepo(ctx.obj["db_path"])
    existing_user = user_repo.get_by_name(name)
    if not existing_user:
        raise ValueError(f"User with name {name} not found")
        
    user_repo.modify(
        models.User(
            id=existing_user.id,  # Preserve the existing ID
            name=name,
            required_protein_per_day=protein,
            required_carbs_per_day=carb,
            required_fat_per_day=fat,
            required_calories_per_day=calories,
        )
    )


@click.command()
@click.option("--name", prompt="User name to delete")
@click.pass_context
def delete(ctx, name):
    user_repo = UserSqliteRepo(ctx.obj["db_path"])
    user_repo.delete_by_name(name)


user.add_command(add, "add")
user.add_command(list_, "list")
user.add_command(update, "update")
user.add_command(delete, "delete")
