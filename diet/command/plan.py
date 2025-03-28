from uuid import uuid4

import click
from tabulate import tabulate

from diet.crud import models
from diet.crud.repo import PlanSqliteRepo
from diet.utils import str_to_snake_case


@click.group()
@click.pass_context
def plan(ctx):
    pass


@click.command()
@click.option("--name", prompt="Plan name")
@click.option("--meals", prompt="Number of meals per day")
@click.option("--days", prompt="Number of days")
@click.option("--portions", prompt="Meal portions per day (format: meal1:portion1,meal2:portion2)")
@click.pass_context
def add(ctx, name, meals, days, portions):
    plan_repo = PlanSqliteRepo(ctx.obj["db_path"])
    name = str_to_snake_case(name)
    
    # Parse portions string into dictionary
    portions_dict = {}
    for portion in portions.split(","):
        meal, portion = portion.split(":")
        portions_dict[meal] = float(portion)
    
    plan_repo.add(
        models.Plan(
            id=str(uuid4()),
            name=name,
            no_of_meal_per_day=int(meals),
            meal_portion_per_day=portions_dict,
            days=int(days),
        )
    )


@click.command()
@click.pass_context
def list_(ctx):
    plan_repo = PlanSqliteRepo(ctx.obj["db_path"])
    plan_list: list[models.Plan] = plan_repo.get_all()
    table = []
    headers = ["name", "meals per day", "days", "portions"]

    for p in plan_list:
        table.append(
            [
                p.name,
                p.no_of_meal_per_day,
                p.days,
                p.meal_portion_per_day,
            ]
        )
    print(tabulate(table, headers=headers))


@click.command()
@click.option("--name", prompt="Plan name to update")
@click.option("--meals", prompt="New number of meals per day")
@click.option("--days", prompt="New number of days")
@click.option("--portions", prompt="New meal portions per day (format: meal1:portion1,meal2:portion2)")
@click.pass_context
def update(ctx, name, meals, days, portions):
    plan_repo = PlanSqliteRepo(ctx.obj["db_path"])
    existing_plan = plan_repo.get_by_name(name)
    if not existing_plan:
        raise ValueError(f"Plan with name {name} not found")
    
    # Parse portions string into dictionary
    portions_dict = {}
    for portion in portions.split(","):
        meal, portion = portion.split(":")
        portions_dict[meal] = float(portion)
    
    plan_repo.modify(
        models.Plan(
            id=existing_plan.id,  # Preserve the existing ID
            name=name,
            no_of_meal_per_day=int(meals),
            meal_portion_per_day=portions_dict,
            days=int(days),
        )
    )


@click.command()
@click.option("--name", prompt="Plan name to delete")
@click.pass_context
def delete(ctx, name):
    plan_repo = PlanSqliteRepo(ctx.obj["db_path"])
    plan_repo.delete_by_name(name)


plan.add_command(add, "add")
plan.add_command(list_, "list")
plan.add_command(update, "update")
plan.add_command(delete, "delete")
