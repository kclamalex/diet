import typing as t
from dataclasses import dataclass
from enum import StrEnum
from enum import auto

from pydantic import BaseModel


class FoodTypeEnum(StrEnum):
    PROTEIN = auto()
    CARBONHYDRATE = auto()


class _Base(BaseModel):
    pass

class NutritionBase(_Base):
    protein_percentage: float
    carbohydrate_percentage: float
    fat_percentage: float

    def get_nutrition_info_tuple(self) -> tuple[float, float, float]:
        return (
            self.protein_percentage,
            self.carbohydrate_percentage,
            self.fat_percentage,
        )


class Food(NutritionBase):
    name: str
    food_type: FoodTypeEnum

    class Config:
        use_enum_values = True



class Consumption(NutritionBase):
    name: str


