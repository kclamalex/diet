import os
import typing as t
from pathlib import Path

import yaml

from diet.crud import models

T = t.TypeVar("T")


class BaseRepo(t.Protocol[T]):

    def get_by_id(self, id_: str) -> T | None: ...

    def get_by_name(self, name: str) -> T | None: ...

    def get_all(self) -> list[T]: ...

    def add(self, entity: list[T]): ...

    def modify(self, entity: T): ...

    def delete_by_id(self, entity_id: str): ...

    def delete_by_name(self, entity_name: str): ...


class FoodRepo(BaseRepo):
    pass


class PlanRepo(BaseRepo):
    pass


class UserRepo(BaseRepo):
    pass


class SubscriptionRepo(BaseRepo):
    pass


class ShoppingList(BaseRepo):
    pass


class BaseYamlRepo(t.Generic[T]):
    def __init__(self, data_folder_path: str, model_class: models.Base):
        self.data_folder_path = data_folder_path
        self.model_class = model_class

    def _get_yaml_files(self) -> list[Path]:
        data_folder_path = Path(self.data_folder_path)
        return list(data_folder_path.glob("**/*.yaml"))

    def _get_yaml_file_by_name(self, entity_name: str) -> Path | None:
        all_yaml_filepaths = self._get_yaml_files()
        for filepath in all_yaml_filepaths:
            name, _ = filepath.stem.rsplit("_", 1)
            if entity_name == name:
                return filepath
        return None

    def _get_yaml_file_by_id(self, entity_id: str) -> Path | None:
        all_yaml_filepaths = self._get_yaml_files()
        for filepath in all_yaml_filepaths:
            _, id_ = filepath.stem.rsplit("_", 1)
            if id_ == entity_id:
                return filepath
        return None

    def _add_yaml_file(self, file_name: str, data_dict: dict) -> Path | None:
        file_path = Path(f"{self.data_folder_path}/{file_name}.yaml")
        if file_path.exists():
            print(f"{file_path} already existed")
            return None
        with open(file_path, "w+") as f:
            yaml.safe_dump(data_dict, f, sort_keys=False)
        return file_path

    def get_by_id(self, id_: str) -> T | None:
        if file_path := self._get_yaml_file_by_id(id_):
            with open(file_path, "r") as f:
                entity_dict = yaml.safe_load(f)
                return self.model_class(**entity_dict)
        return None

    def get_by_name(self, name: str) -> T | None:
        if file_path := self._get_yaml_file_by_name(name):
            with open(file_path, "r") as f:
                entity_dict = yaml.safe_load(f)
                return self.model_class(**entity_dict)
        return None

    def get_all(self, **filter) -> list[T]:
        entities = []
        all_yaml_files = self._get_yaml_files()
        for file in all_yaml_files:
            with open(file, "r") as f:
                entity_dict = yaml.safe_load(f)
                if all([entity_dict[k] == v for k, v in filter.items()]):
                    entities.append(self.model_class(**entity_dict))
        return entities

    def add(self, entity: T):
        if getattr(entity, "name", None) is not None:
            file_name = f"{entity.name}_{entity.id}"
        else:
            file_name = entity.id
        _ = self._add_yaml_file(file_name, entity.dict())

    def modify(self, entity: T):
        raise NotImplementedError

    def delete_by_id(self, entity_id: str):
        file_path = self._get_yaml_file_by_id(entity_id)
        if file_path is None:
            raise ValueError(f"{entity_id} doesn't exist")
        os.remove(file_path)

    def delete_by_name(self, entity_name: str):
        file_path = self._get_yaml_file_by_name(entity_name)
        if file_path is None:
            raise ValueError(f"{entity_name} doesn't exist")
        os.remove(file_path)


class FoodYamlRepo(BaseYamlRepo[models.Food]):
    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/food"
        super().__init__(self.data_folder_path, models.Food)


class PlanYamlRepo(BaseYamlRepo[models.Plan]):
    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/plan"
        super().__init__(self.data_folder_path, models.Plan)


class UserYamlRepo(BaseYamlRepo[models.User]):
    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/user"
        super().__init__(self.data_folder_path, models.User)


class SubscriptionYamlRepo(BaseYamlRepo[models.Subscription]):
    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/subscription"
        super().__init__(self.data_folder_path, models.Subscription)


class ShoppingListYamlRepo(BaseYamlRepo[models.ShoppingList]):
    def __init__(self, data_folder_path: str):
        self.data_folder_path = data_folder_path + "/shopping_list"
        super().__init__(self.data_folder_path, models.ShoppingList)
