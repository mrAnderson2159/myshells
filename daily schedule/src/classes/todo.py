from src.interfaces.validate import Validate
from src.classes.enums import FrequencyEnum
from typing import Union, List, Tuple
from datetime import datetime
from debug import debug


class Todo(Validate):
    def __init__(self, task: str, frequency: FrequencyEnum, day: int, repetition: Tuple[int] = (0,)):
        """ This class is used to instantiate an object representing a task to be executed.

        :param task: description
        :param frequency: fixed or occasional
        :param day: weekday for fixed todos, year-day for occasional
        :param repetition: Optional, set to 0 as default if the todo
        is fixed then this will represent how many weeks passes between
        each repetition, if it's occasional this will represent days
        """
        self.validate_params_ex((task, frequency, day, tuple(repetition)),
                                (str, FrequencyEnum, int, tuple))

        self.task = task
        self.frequency = frequency
        self.day = day
        self.repetition = repetition
        self.record_date = datetime.now().isoformat()

    @classmethod
    def fromdict(cls, todo_dict: dict, frequency: FrequencyEnum) -> 'Todo':
        cls.validate_params_ex(todo_dict, dict)
        task = todo_dict['task']
        day = todo_dict['day']
        rep = todo_dict['rep']
        return cls(task, frequency, day, rep)

    def rename(self, task: str):
        self.validate_params_ex(task, str)
        self.task = task

    def change(self, *, task: str = None, repetition: Union[tuple, int] = None):
        if task is not None:
            self.rename(task)
        if repetition is not None:
            self.repetition = repetition

    def __check(self, other) -> None:
        self.validate_params_ex(other, Todo)
        if other.frequency != self.frequency:
            raise TypeError(f"Cannot compare {self.frequency.name} with {other.frequency.name} todo")

    def __str__(self):
        return self.task

    def __repr__(self):
        return str(self)

    def __lt__(self, other: 'Todo') -> bool:
        self.__check(other)
        return self.day < other.day

    def __le__(self, other: 'Todo') -> bool:
        self.__check(other)
        return self.day <= other.day

    def __gt__(self, other: 'Todo') -> bool:
        self.__check(other)
        return self.day > other.day

    def __ge__(self, other: 'Todo') -> bool:
        self.__check(other)
        return self.day >= other.day

    def __eq__(self, other: 'Todo') -> bool:
        self.__check(other)
        return self.day == other.day

    def equals(self, other: 'Todo') -> bool:
        return self.task == other.task \
               and self.frequency == other.frequency \
               and self.day == other.day


if __name__ == '__main__':
    t1 = Todo('mario', FrequencyEnum.FIXED, 3)
    t2 = Todo('luca', FrequencyEnum.OCCASIONAL, 2)

    print(t2 < t1)
