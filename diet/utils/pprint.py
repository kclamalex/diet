from crud import models
from tabulate import tabulate

__all__ = [
    "print_food_list",
]


def print_food_list(food_list: list[models.Food]):
    table = []
    headers = [
        "name",
        "type",
        "protein per 1 g",
        "carbs per 1 g",
        "fat per 1 g",
        "calories per 1 g",
    ]

    for f in food_list:
        table.append(
            [
                f.name,
                f.food_type,
                f.protein_percentage,
                f.carbohydrate_percentage,
                f.fat_percentage,
                f.calories_per_g,
            ]
        )
    print(tabulate(table, headers=headers))


def print_day_plan(diet_plan: models.DailyDietPlan):
    pass


# def print_one_meal_portion_per_people(food_name: str, food_repo: FoodRepo):
#
#
#     protein_one_meal_portion_gram = protein_needed_per_day / num_of_meals
#     carbs_one_meal_portion_gram = carbs_needed_per_day / num_of_meals
#
#     print(
#         f"portion needed for one meal per people"
#         f" - {protein.name}: {protein_one_meal_portion_gram}g, {carbohydrate.name}: {carbs_one_meal_portion_gram}g"
#     )
#
#     print(
#         f"portion needed for one meal for {num_of_ppl} people"
#         f" - {protein.name}: {protein_one_meal_portion_gram * num_of_ppl}g, {carbohydrate.name}: {carbs_one_meal_portion_gram * num_of_ppl}g"
#     )
#     print(
#         f"portion needed per day for {num_of_meals} meal for {num_of_ppl} people"
#         f" - {protein.name}: {protein_needed_per_day * num_of_ppl}g, {carbohydrate.name}: {carbs_needed_per_day * num_of_ppl}g"
#     )
#     print(
#         f"portion needed for {num_of_meals} meal for {days_of_week} days for {num_of_ppl} people"
#         f" - {protein.name}: {protein_needed_per_day * days_of_week * num_of_ppl}g, {carbohydrate.name}: {carbs_needed_per_day * days_of_week * num_of_ppl}g"
#     )
#     protein_a_cycle = (protein_one_meal_portion_gram * days_of_week *
#                        num_of_meals * num_of_ppl)
#     carbs_a_cycle = (carbs_one_meal_portion_gram * days_of_week *
#                      num_of_meals * num_of_ppl)
#
#     if protein.name == "egg":
#         avg_gram_per_egg = 68
#         num_of_egg = ceil(protein_a_cycle / avg_gram_per_egg)
#         shopping_list[protein.name] += num_of_egg
#         result = (
#             f"{protein.name}: {num_of_egg}, {carbohydrate.name}: {carbs_a_cycle}g"
#         )
#     else:
#         shopping_list[protein.name] += protein_a_cycle
#
#     shopping_list[carbohydrate.name] += carbs_a_cycle
