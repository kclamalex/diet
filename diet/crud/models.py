import datetime as dt
import uuid
from enum import StrEnum

from pydantic import BaseModel

__all__ = [
    "Base",
    "FoodTypeEnum",
    "Food",
    "Protein",
    "Carbs",
    "Vegs",
    "Plan",
    "Subscription",
]


class FoodTypeEnum(StrEnum):
    PROTEIN = "protein"
    CARBS = "carbs"
    VEGS = "vegs"


class Base(BaseModel):
    id: str | None = str(uuid.uuid4())
    created_at: dt.datetime | None = dt.datetime.now(dt.timezone.utc)


class Food(Base):
    name: str
    food_type: FoodTypeEnum
    protein_per_gram: float
    carbs_per_gram: float
    fat_per_gram: float
    calories_per_gram: float

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
        super().__init__(
            **data,
        )


class User(Base):
    name: str
    required_protein_per_day: float
    required_carbs_per_day: float
    required_fat_per_day: float
    required_calories_per_day: float


class Plan(Base):
    name: str
    no_of_meal_per_day: int
    meal_portion_per_day: dict[str, float]
    days: int


class Subscription(Base):
    user_id: str
    diet_plan_id: str


class ShoppingList(Base):
    diet_plan_ids: list[str]
    shopping_list: dict[str, float]
