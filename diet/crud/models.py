import typing as t
from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel


class FoodTypeEnum(StrEnum):
    PROTEIN = "protein"
    CARBS = "carbs"
    VEGS = "vegs"


class _Base(BaseModel):
    pass


class NutritionBase(_Base):
    protein_percentage: float
    carbohydrate_percentage: float
    fat_percentage: float
    calories_per_g: float

    def get_nutrition_info_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.protein_percentage,
            self.carbohydrate_percentage,
            self.fat_percentage,
            self.calories_per_g,
        )


class Food(NutritionBase):
    name: str
    food_type: FoodTypeEnum

    class Config:
        use_enum_values = True
    def __repr__(self) -> str:
        return self.name
    def __str__(self) -> str:
        return self.name

class Protein(Food):

    def __init__(self, **data):
        data.update({"food_type": FoodTypeEnum.PROTEIN})
        super().__init__(**data)


class Carbs(Food):

    def __init__(self, **data):
        data.update({"food_type": FoodTypeEnum.CARBS})
        super().__init__(**data)


class Vegs(Food):

    def __init__(self, **data):
        data.update({"food_type": FoodTypeEnum.VEGS})
        super().__init__(**data, )


class User(NutritionBase):
    name: str


class DailyDietPlan(_Base):
    user: User
    meal_portion_per_day: dict[str, float]

    def get_meal_portion_per_meal(self, num_of_meal: int) -> dict[str, float]:
        return {
            food_name: meal_portion_per_day / num_of_meal
            for food_name, meal_portion_per_day in
            self.meal_portion_per_day.items()
        }
