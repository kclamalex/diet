import typing as t

import click

END = "Press enter again to end this prompt"


def collect_entities_from_user_input_until_the_end(
    question: str, getter: t.Callable
) -> list[t.Any]:
    res = []
    while user_input := click.prompt(
        question,
        default=END,
    ):
        if user_input == END:
            break
        try:
            entity = getter(user_input)
        except Exception as e:
            click.echo(f"Unknown errors happened: {e}")
        if entity is None:
            click.echo(f"{user_input} doesn't exist")
            continue
        res.append(entity)
    return res
