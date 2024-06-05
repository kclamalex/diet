import os
import typing as t
from pathlib import Path

import yaml
from thefuzz import fuzz

from crud.models import Food
from crud.models import Consumption
T = t.TypeVar("T")


class NutritionRepo(t.Protocol[T]):

    def get(self, name: str) -> T | None:
        ...

    def get_all(self) -> list[T]:
        ...

    def add(self, entity: list[T]):
        ...

    def modify(self, entity: T):
        ...

    def delete(self, entity: T):
        ...


class FoodRepo(NutritionRepo):
    ...


class ConsumptionRepo(NutritionRepo):
    ...


class FoodYamlRepo:

    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/food"

    def _get_yaml_files(self) -> list[Path]:
        data_folder_path = Path(self.data_folder_path)
        return list(data_folder_path.glob("**/*.yaml"))

    def _get_yaml_file_by_name(self, name_to_search: str) -> Path | None:
        all_yaml_filepaths = self._get_yaml_files()
        for filepath in all_yaml_filepaths:
            food_name = filepath.stem
            if fuzz.ratio(name_to_search, food_name) >= 80:
                return filepath
        return None

    def get(self, name: str) -> Food | None:
        if file_path := self._get_yaml_file_by_name(name):
            with open(file_path, 'r') as f:
                food_dict = yaml.safe_load(f)
                return Food(**food_dict)
        return None

    def get_all(self) -> list[Food]:
        foods = []
        all_yaml_files = self._get_yaml_files()
        for file in all_yaml_files:
            with open(file, "r") as f:
                food_dict = yaml.safe_load(f)
                foods.append(Food(**food_dict))
        return foods

    def add(self, foods: list[Food]):
        for food in foods:
            file_path = Path(f"{self.data_folder_path}/{food.name}.yaml")
            if file_path.exists():
                print(f"{file_path} already existed")
                continue
            with open(file_path, "w+") as f:
                yaml.safe_dump(food.dict(), f)

    def modify(self, food: Food):
        self.delete(food)
        self.add([food])

    def delete(self, food: Food):
        file_path = self._get_yaml_file_by_name(food.name)
        if file_path is None:
            raise ValueError(f"{food.name} doesn't exist")
        os.remove(file_path)


class ConsumptionYamlRepo:

    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/consumption"

    def _get_yaml_files(self) -> list[Path]:
        data_folder_path = Path(self.data_folder_path)
        return list(data_folder_path.glob("**/*.yaml"))

    def _get_yaml_file_by_name(self, name_to_search: str) -> Path | None:
        all_yaml_filepaths = self._get_yaml_files()
        for filepath in all_yaml_filepaths:
            consumption_name = filepath.stem
            if fuzz.ratio(name_to_search, consumption_name) >= 80:
                return filepath
        return None

    def get(self, name: str) -> Consumption | None:
        if file_path := self._get_yaml_file_by_name(name):
            with open(file_path, 'r') as f:
                consumption_dict = yaml.safe_load(f)
                return Consumption(**consumption_dict)
        return None

    def get_all(self) -> list[Consumption]:
        consumptions = []
        all_yaml_files = self._get_yaml_files()
        for file in all_yaml_files:
            with open(file, "r") as f:
                consumption_dict = yaml.safe_load(f)
                consumptions.append(Consumption(**consumption_dict))
        return consumptions

    def add(self, consumptions: list[Consumption]):
        for consumption in consumptions:
            file_path = Path(
                f"{self.data_folder_path}/{consumption.name}.yaml")
            if file_path.exists():
                print(f"{file_path} already existed")
                continue
            with open(file_path, "w+") as f:
                yaml.safe_dump(consumption.dict(), f)

    def modify(self, consumption: Consumption):
        self.delete(consumption)
        self.add([consumption])

    def delete(self, consumption: Consumption):
        file_path = self._get_yaml_file_by_name(consumption.name)
        if file_path is None:
            raise ValueError(f"{consumption.name} doesn't exist")
        os.remove(file_path)
