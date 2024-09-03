import click
from tabulate import tabulate

from diet.crud import models
from diet.crud.repo import (
    FoodYamlRepo,
    PlanYamlRepo,
    SubscriptionYamlRepo,
    UserYamlRepo,
)
from diet.logic import DietPlan
from diet.utils.prompt import collect_entities_from_user_input_until_the_end
from diet.utils.strutils import str_to_snake_case


@click.group()
@click.pass_context
def plan(ctx):
    pass


@click.command()
@click.option("--name", prompt="Plan name")
@click.option(
    "--meal",
    prompt="How many meal you would like to have per day",
    type=click.INT,
)
@click.option(
    "--days", prompt="How many days you would like to plan", type=click.INT
)
@click.pass_context
def add(ctx, name, meal, days):
    food_list = []
    food_repo = FoodYamlRepo(ctx.obj["data_folder_path"])
    user_repo = UserYamlRepo(ctx.obj["data_folder_path"])
    diet_plan_repo = PlanYamlRepo(ctx.obj["data_folder_path"])
    subscription_repo = SubscriptionYamlRepo(ctx.obj["data_folder_path"])
    diet_plan_logic = DietPlan(food_repo)
    rand = click.prompt(
        "Do you want to generate food combinations randomly (Y/n)?",
        type=click.BOOL,
    )
    if rand:
        food_list = diet_plan_logic.get_random_food_combination(meal)[0]
    else:
        food_list = collect_entities_from_user_input_until_the_end(
            "Please enter food you would like to eat to generate the plan",
            food_repo.get_by_name,
        )

    user = collect_entities_from_user_input_until_the_end(
        "Please enter user you would like to use to generate the plan",
        user_repo.get_by_name,
    )
    user = user[0]
    if not food_list or not user:
        print(
            "You didn't enter food or diet_plan to generate diet plan."
            "Please try to enter them again"
        )
        return

    meal_portion_per_day = diet_plan_logic.get_meal_portion_per_day_in_gram(
        food_list, user
    )

    diet_plan = models.Plan(
        name=str_to_snake_case(name),
        no_of_meal_per_day=meal,
        days=days,
        meal_portion_per_day=meal_portion_per_day,
    )

    diet_plan_repo.add(diet_plan)

    subscription_repo.add(
        models.Subscription(user_id=user.id, diet_plan_id=diet_plan.id)
    )


@click.command()
@click.pass_context
def list_(ctx):
    diet_plan_repo = PlanYamlRepo(ctx.obj["data_folder_path"])
    diet_plans = diet_plan_repo.get_all()
    table = []
    headers = [
        "id",
        "name",
        "created at",
        "no. of meal per day",
        "meal portion per day",
        "portion per meal",
    ]

    for dp in diet_plans:
        table.append(
            [
                dp.id,
                dp.name,
                dp.created_at,
                dp.no_of_meal_per_day,
                dp.meal_portion_per_day,
                {
                    k: v / dp.no_of_meal_per_day
                    for k, v in dp.meal_portion_per_day.items()
                },
            ]
        )
    print(tabulate(table, headers=headers))


@click.command()
@click.option("--name", prompt="Plan name to delete")
@click.pass_context
def delete(ctx, name):
    name = str_to_snake_case(name)
    diet_plan_repo = PlanYamlRepo(ctx.obj["data_folder_path"])
    subscription_repo = SubscriptionYamlRepo(ctx.obj["data_folder_path"])
    plan = diet_plan_repo.get_by_name(name)
    if plan is None:
        raise ValueError(f"Plan {name} doesn't exist")
    subscriptions = subscription_repo.get_all()
    for s in subscriptions:
        if s.diet_plan_id == plan.id:
            subscription_repo.delete_by_id(s.id)
    diet_plan_repo.delete_by_id(plan.id)


plan.add_command(add, "add")
plan.add_command(list_, "list")
plan.add_command(delete, "delete")
