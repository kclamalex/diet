import random
import typing as t

__all__ = ["unique_choice"]


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


