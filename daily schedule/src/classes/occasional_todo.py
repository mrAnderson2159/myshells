from src.classes.todo import Todo
from src.classes.enums import FrequencyEnum
from typing import Union


class OccasionalTodo(Todo):
    def __init__(self, task: str, day: int, repetition: Union[int, tuple] = (0,)):
        super().__init__(task, FrequencyEnum.OCCASIONAL, day, repetition)
