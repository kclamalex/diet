from uuid import uuid4

import click
from tabulate import tabulate

from diet.crud import models
from diet.crud.repo import ShoppingListSqliteRepo, PlanSqliteRepo
from diet.utils import str_to_snake_case


@click.group()
@click.pass_context
def shop(ctx):
    pass


@click.command()
@click.option("--name", prompt="Shopping list name")
@click.option("--plans", prompt="Plan IDs (comma separated)")
@click.pass_context
def add(ctx, name, plans):
    shopping_list_repo = ShoppingListSqliteRepo(ctx.obj["db_path"])
    plan_repo = PlanSqliteRepo(ctx.obj["db_path"])
    name = str_to_snake_case(name)
    
    # Parse plan IDs
    plan_ids = [pid.strip() for pid in plans.split(",")]
    
    # Validate plans exist
    shopping_list = {}
    for plan_id in plan_ids:
        plan = plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError(f"Plan with ID {plan_id} not found")
        # Merge plan portions into shopping list
        for food, amount in plan.meal_portion_per_day.items():
            shopping_list[food] = shopping_list.get(food, 0) + amount * plan.days
    
    shopping_list_repo.add(
        models.ShoppingList(
            id=str(uuid4()),
            name=name,
            diet_plan_ids=plan_ids,
            shopping_list=shopping_list,
        )
    )


@click.command()
@click.pass_context
def list_(ctx):
    shopping_list_repo = ShoppingListSqliteRepo(ctx.obj["db_path"])
    shopping_lists: list[models.ShoppingList] = shopping_list_repo.get_all()
    table = []
    headers = ["name", "plan IDs", "shopping list"]

    for sl in shopping_lists:
        table.append(
            [
                sl.name,
                sl.diet_plan_ids,
                sl.shopping_list,
            ]
        )
    print(tabulate(table, headers=headers))


@click.command()
@click.option("--name", prompt="Shopping list name to update")
@click.option("--plans", prompt="New plan IDs (comma separated)")
@click.pass_context
def update(ctx, name, plans):
    shopping_list_repo = ShoppingListSqliteRepo(ctx.obj["db_path"])
    plan_repo = PlanSqliteRepo(ctx.obj["db_path"])
    
    existing_list = shopping_list_repo.get_by_name(name)
    if not existing_list:
        raise ValueError(f"Shopping list with name {name} not found")
    
    # Parse plan IDs
    plan_ids = [pid.strip() for pid in plans.split(",")]
    
    # Validate plans exist and calculate new shopping list
    shopping_list = {}
    for plan_id in plan_ids:
        plan = plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError(f"Plan with ID {plan_id} not found")
        # Merge plan portions into shopping list
        for food, amount in plan.meal_portion_per_day.items():
            shopping_list[food] = shopping_list.get(food, 0) + amount * plan.days
    
    shopping_list_repo.modify(
        models.ShoppingList(
            id=existing_list.id,  # Preserve the existing ID
            name=name,
            diet_plan_ids=plan_ids,
            shopping_list=shopping_list,
        )
    )


@click.command()
@click.option("--name", prompt="Shopping list name to delete")
@click.pass_context
def delete(ctx, name):
    shopping_list_repo = ShoppingListSqliteRepo(ctx.obj["db_path"])
    shopping_list_repo.delete_by_name(name)


shop.add_command(add, "add")
shop.add_command(list_, "list")
shop.add_command(update, "update")
shop.add_command(delete, "delete")
