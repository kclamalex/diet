from dataclasses import dataclass
from enum import StrEnum
from enum import auto
from itertools import product
from math import ceil

import numpy as np
from scipy.optimize import nnls


class FoodType(StrEnum):
    PROTEIN = auto()
    CARBONHYDRATE = auto()


@dataclass
class NutritionBase:
    protein_percentage: float
    carbohydrate_percentage: float
    fat_percentage: float

    def get_nutrition_info_tuple(self) -> tuple[float, float, float]:
        return (
            self.protein_percentage,
            self.carbohydrate_percentage,
            self.fat_percentage,
        )


@dataclass
class FoodBase(NutritionBase):
    name: str
    type: FoodType


@dataclass
class Consumption(NutritionBase):
    name: str


class Protein(FoodBase):
    def __init__(self, *args, **kwargs):
        super().__init__(type=FoodType.PROTEIN, *args, **kwargs)

    def __repr__(self) -> str:
        return self.name


class Carbohydrate(FoodBase):
    def __init__(self, *args, **kwargs):
        super().__init__(type=FoodType.CARBONHYDRATE, *args, **kwargs)

    def __repr__(self) -> str:
        return self.name


if __name__ == "__main__":
    chicken_breast = Protein(
        name="chicken_breast",
        protein_percentage=0.62,
        carbohydrate_percentage=0,
        fat_percentage=0.05,
    )
    shrimp = Protein(
        name="shrimp",
        protein_percentage=0.48,
        carbohydrate_percentage=0,
        fat_percentage=0.05,
    )
    salmon = Protein(
        name="salmon",
        protein_percentage=0.4,
        carbohydrate_percentage=0,
        fat_percentage=0.2,
    )
    egg = Protein(
        name="egg",
        protein_percentage=0.26,
        carbohydrate_percentage=0,
        fat_percentage=0.16,
    )
    rice = Carbohydrate(
        name="rice",
        protein_percentage=0.05,
        carbohydrate_percentage=0.89,
        fat_percentage=0,
    )
    potato = Carbohydrate(
        name="potato",
        protein_percentage=0,
        carbohydrate_percentage=0.73,
        fat_percentage=0,
    )
    sweet_potato = Carbohydrate(
        name="sweet_potato",
        protein_percentage=0.03,
        carbohydrate_percentage=0.92,
        fat_percentage=0,
    )
    consumption = Consumption(
        name="me",
        protein_percentage=120.25,
        carbohydrate_percentage=163,
        fat_percentage=65,
    )

    proteins = [chicken_breast, shrimp, salmon, egg]
    carbohydrates = [rice, potato, sweet_potato]

    combinations = list(product(proteins, carbohydrates))

    for protein, carbohydrate in combinations:
        x = np.array(
            [
                protein.get_nutrition_info_tuple(),
                carbohydrate.get_nutrition_info_tuple(),
            ]
        )
        y = np.array(consumption.get_nutrition_info_tuple())

        A = np.vstack([x]).T
        m = nnls(A, y)[0]

        result = f"{protein.name}: {ceil(m[0])}g, {carbohydrate.name}: {ceil(m[1])}g"
        print(result)
# 4 types of protein
# 1. Chicken Breast
# 2. Salmon
# 3. Shrimp
# 4. Egg

# 3 types of carbohydrates:
# 1. Rice
# 2. Potato mashes
# 3. Sweet potato

# 4 types of vegetables:
# 1. Broccoli
# 2. Spinach
# 3. Watercress
# 4. Chinese cabbage

# Daily diet for 65kg:
# Carbohydrates: 163g
# Protein: 120.25g
# Fat: 65g
