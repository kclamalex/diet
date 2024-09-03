from collections import defaultdict

import click
from tabulate import tabulate

from diet.crud import models
from diet.crud.repo import PlanYamlRepo, ShoppingListYamlRepo
from diet.utils.prompt import collect_entities_from_user_input_until_the_end


@click.group()
@click.pass_context
def shop(ctx):
    pass


@click.command()
@click.pass_context
def add(ctx):
    diet_plan_repo = PlanYamlRepo(ctx.obj["data_folder_path"])
    shopping_list_repo = ShoppingListYamlRepo(ctx.obj["data_folder_path"])
    plan_list = collect_entities_from_user_input_until_the_end(
        "Please enter plan you would like to add to generate the shopping list",
        diet_plan_repo.get_by_name,
    )

    shopping_list_dict = defaultdict(float)
    plan_ids = []
    for plan in plan_list:
        plan_ids.append(plan.id)
        for food_name, gram in plan.meal_portion_per_day.items():
            shopping_list_dict[food_name] += gram

    shopping_list = models.ShoppingList(
        diet_plan_ids=plan_ids, shopping_list=shopping_list_dict
    )
    shopping_list_repo.add(shopping_list)


@click.command()
@click.pass_context
def list_(ctx):
    shopping_list_repo = ShoppingListYamlRepo(ctx.obj["data_folder_path"])
    shopping_lists = shopping_list_repo.get_all()
    table = []
    headers = [
        "id",
        "created at",
        "diet plan ids",
        "shopping list",
    ]

    for sl in shopping_lists:
        table.append(
            [
                sl.id,
                sl.created_at,
                sl.diet_plan_ids,
                sl.shopping_list,
            ]
        )
    print(tabulate(table, headers=headers))


shop.add_command(add, "add")
shop.add_command(list_, "list")
