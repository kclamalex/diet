__all__ = ["str_to_snake_case"]


def str_to_snake_case(str_: str) -> str:
    return str_.lower().replace(" ", "_")
