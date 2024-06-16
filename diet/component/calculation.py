from math import ceil

import numpy as np
from scipy.optimize import nnls

from crud import models

def get_meal_portion_per_day_in_gram(
        food_list: list[models.Food],
        consumption_list: list[models.Consumption]
) -> dict[str, models.DietPlan]:

    meal_portion_per_day_by_user = {}
    foods_matrix = np.array([f.get_nutrition_info_tuple() for f in food_list])

    foods_transposed_matrix = np.vstack([foods_matrix]).T

    for user in consumption_list:
        grams_needed_per_day = nnls(foods_transposed_matrix,
                                    user.get_nutrition_info_tuple())[0]
        meal_portion_per_day = {
            food.name: ceil(g_per_day)
            for food, g_per_day in zip(food_list, grams_needed_per_day)
        }

        meal_portion_per_day_by_user[user.name] = models.DietPlan(
            user=user, meal_portion_per_day=meal_portion_per_day)

    return meal_portion_per_day_by_user
