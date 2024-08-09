from src.classes.todo import Todo
from src.classes.enums import FrequencyEnum
from typing import Union, Tuple


class FixedTodo(Todo):
    def __init__(self, task: str, day: int, repetition: Tuple[int]):
        if isinstance(repetition, Tuple) and not len(repetition):
            raise ValueError("Fixed Todo must repeat")
        if not 0 <= day < 7:
            raise ValueError(f"The day parameter for fixed todos must be a weekday, {day} is not valid")
        super().__init__(task, FrequencyEnum.FIXED, day, repetition)

    @classmethod
    def fromdict(cls, todo_dict: dict, **kwargs) -> 'FixedTodo':
        return cls(**todo_dict)

