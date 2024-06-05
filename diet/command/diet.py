import click

from crud.repo import FoodYamlRepo, ConsumptionYamlRepo
from component.calculation import get_meal_portion_per_day_in_gram

END = "Press enter again to end this prompt"


@click.command()
@click.pass_context
def plan(ctx):
    food_list = []
    consumption_list = []
    food_repo = FoodYamlRepo(ctx.obj["data_folder_path"])
    consumption_repo = ConsumptionYamlRepo(ctx.obj["data_folder_path"])

    all_food = food_repo.get_all()
    while food_name := click.prompt(
            "Please enter food you would like to eat to generate the plan",
            default=END):
        if food_name == END:
            break
        if food_name not in [f.name for f in all_food]:
            print(f"{food_name} nutrition info doesn't exist")
            continue
        food = food_repo.get(food_name)
        food_list.append(food)

    all_consumptions = consumption_repo.get_all()
    while user_name := click.prompt(
            "Please enter user you would like to use to generate the plan",
            default=END):
        if user_name == END:
            break
        if user_name not in [u.name for u in all_consumptions]:
            print(f"{user_name} nutrition info doesn't exist")
            continue
        consumption = consumption_repo.get(user_name)
        consumption_list.append(consumption)

    if not food_list or not consumption_list:
        print(
            "You didn't enter food or user to generate diet plan. Please try to enter them again"
        )
        return

    result = get_meal_portion_per_day_in_gram(food_list, consumption_list)
