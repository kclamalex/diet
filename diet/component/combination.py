import typing as t
from itertools import product
import random


def unique_choice(elements: list[t.Any], k: int) -> list:
    if not elements:
        return []
    choices: list[t.Any] = []
    selected = []
    while len(choices) < k:
        idx = random.randint(0, len(elements) - 1)
        if idx not in selected:
            choices.append(elements[idx])
            selected.append(idx)
    return choices


def pick_k_unique_food_combinations(proteins: list, carbs: list, vegs: list,
                                    k: int) -> list:
    args = [proteins, carbs, vegs]
    args = list(filter(lambda x: len(x) > 0, args))
    combinations = list(product(*args))
    return unique_choice(combinations, k)
