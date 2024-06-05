from itertools import product
from math import ceil
import random

import numpy as np
from scipy.optimize import nnls


def unique_choice(elements: list, k: int) -> list:
    choices = []
    selected = []
    while len(choices) < k:
        idx = random.randint(0, len(elements) - 1)
        if idx not in selected:
            choices.append(elements[idx])
            selected.append(idx)
    return choices


def pick_k_unique_food_combinations(proteins: list, carbs: list,
                                    k: int) -> list:
    combinations = list(product(proteins, carbs))
    return unique_choice(combinations, k)


def get_meal_portion_per_day_in_gram(
        food_list: list[models.Food],
        consumption: models.Consumption) -> dict[str:int]:

    foods_matrix = np.array([f.get_nutrition_info_tuple() for f in food_list])

    consumption_matrix = np.array(consumption.get_nutrition_info_tuple())

    foods_transposed_matrix = np.vstack([foods_matrix]).T

    grams_needed_per_day = nnls(foods_transposed_matrix, consumption_matrix)[0]

    return {
            food.name: ceil(g_per_day)
        for food, g_per_day in zip(food_list, grams_needed_per_day)
    }


def get_one_meal_portion_in_gram(
    protein_grams_needed_per_day: float,
    carbs_grams_needed_per_day: float,
    num_of_meals_per_day: int,
):
    return (
        protein_grams_needed_per_day / num_of_meals_per_day,
        carbs_grams_needed_per_day / num_of_meals_per_day,
    )


