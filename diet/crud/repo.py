import os
import typing as t
from pathlib import Path

import yaml
from thefuzz import fuzz

from crud.models import Food
from crud.models import User

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

    def delete(self, entity_name: str):
        ...


class FoodRepo(NutritionRepo):
    ...


class UserRepo(NutritionRepo):
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

    def get_all(self, **filter) -> list[Food]:
        foods = []
        all_yaml_files = self._get_yaml_files()
        for file in all_yaml_files:
            with open(file, "r") as f:
                food_dict = yaml.safe_load(f)
                if all([food_dict[k] == v for k, v in filter.items()]):
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
        self.delete(food.name)
        self.add([food])

    def delete(self, food_name: str):
        file_path = self._get_yaml_file_by_name(food_name)
        if file_path is None:
            raise ValueError(f"{food_name} doesn't exist")
        os.remove(file_path)


class UserYamlRepo:

    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/user"

    def _get_yaml_files(self) -> list[Path]:
        data_folder_path = Path(self.data_folder_path)
        return list(data_folder_path.glob("**/*.yaml"))

    def _get_yaml_file_by_name(self, name_to_search: str) -> Path | None:
        all_yaml_filepaths = self._get_yaml_files()
        for filepath in all_yaml_filepaths:
            user_name = filepath.stem
            if fuzz.ratio(name_to_search, user_name) >= 80:
                return filepath
        return None

    def get(self, name: str) -> User | None:
        if file_path := self._get_yaml_file_by_name(name):
            with open(file_path, 'r') as f:
                user_dict = yaml.safe_load(f)
                return User(**user_dict)
        return None

    def get_all(self) -> list[User]:
        users = []
        all_yaml_files = self._get_yaml_files()
        for file in all_yaml_files:
            with open(file, "r") as f:
                user_dict = yaml.safe_load(f)
                users.append(User(**user_dict))
        return users

    def add(self, users: list[User]):
        for user in users:
            file_path = Path(
                f"{self.data_folder_path}/{user.name}.yaml")
            if file_path.exists():
                print(f"{file_path} already existed")
                continue
            with open(file_path, "w+") as f:
                yaml.safe_dump(user.dict(), f)

    def modify(self, user: User):
        self.delete(user.name)
        self.add([user])

    def delete(self, username: str):
        file_path = self._get_yaml_file_by_name(username)
        if file_path is None:
            raise ValueError(f"{username} doesn't exist")
        os.remove(file_path)
