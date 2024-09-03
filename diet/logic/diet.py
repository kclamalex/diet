from itertools import product
from math import ceil

import numpy as np
from scipy.optimize import nnls

from diet.crud import FoodYamlRepo, models
from diet.utils import combination

__all__ = ["DietPlan"]


class DietPlan:
    def __init__(
        self,
        food_repo: FoodYamlRepo,
    ):
        self.food_repo = food_repo

    def get_random_food_combination(
        self, no_of_combinations: int
    ) -> list[models.Food]:
        all_proteins = self.food_repo.get_all(**{"food_type": "protein"})
        all_carbs = self.food_repo.get_all(**{"food_type": "carbs"})
        all_vegs = self.food_repo.get_all(**{"food_type": "vegs"})
        args = [all_proteins, all_carbs, all_vegs]
        args = list(filter(lambda x: len(x) > 0, args))
        combinations = list(product(*args))
        return combination.unique_choice(combinations, no_of_combinations)

    def get_meal_portion_per_day_in_gram(
        self,
        food_list: list[models.Food],
        user: models.User,
    ) -> dict[str, float]:
        # First perserve 10% calories for vegatbles
        required_calories_per_day = user.required_calories_per_day * 0.9
        required_fat_per_day = user.required_fat_per_day
        required_carbs_per_day = user.required_carbs_per_day
        required_protein_per_day = user.required_protein_per_day
        # Get vegetable out of the food list and deduct the nutrients
        food_nutrient_matrix = []
        food_without_vegs = []
        vegs = None
        for f in food_list:
            if f.food_type == models.FoodTypeEnum.VEGS:
                vegs = f
                gram_of_vegs_intake = (
                    user.required_calories_per_day * 0.1 / f.calories_per_gram
                )
                required_fat_per_day -= f.fat_per_gram * gram_of_vegs_intake
                required_protein_per_day -= (
                    f.protein_per_gram * gram_of_vegs_intake
                )
                required_carbs_per_day -= (
                    f.carbs_per_gram * gram_of_vegs_intake
                )
            else:
                food_without_vegs.append(f)
                food_nutrient_matrix.append(
                    (
                        f.calories_per_gram,
                        f.fat_per_gram,
                        f.protein_per_gram,
                        f.carbs_per_gram,
                    )
                )
        food_nutrient_matrix = np.array(food_nutrient_matrix)
        consumption_matrix = np.array(
            (
                required_calories_per_day,
                required_fat_per_day,
                required_protein_per_day,
                required_carbs_per_day,
            )
        )

        food_transposed_matrix = np.vstack([food_nutrient_matrix]).T

        grams_needed_per_day = nnls(
            food_transposed_matrix, consumption_matrix
        )[0]
        res = {}

        if vegs:
            res[vegs.name] = gram_of_vegs_intake

        for food, gram_per_day in zip(food_without_vegs, grams_needed_per_day):
            res[food.name] = ceil(gram_per_day)
        return res
