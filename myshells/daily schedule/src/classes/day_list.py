__all__ = ["EmptyDayException", "DayList"]


from src.interfaces.validate import Validate
from src.classes.occasional_todo import OccasionalTodo
from typing import List, Dict, Optional, Tuple
from colors import yellow
from inspect import stack
from debug import debug


class EmptyDayException(Exception):
    """Raised when trying to accede an empty day"""


class DayList(Validate):
    def __init__(self):
        self.__daylist: Dict[int, List[OccasionalTodo]] = {}

    @classmethod
    def fromdict(cls, daylist_dict: dict) -> 'DayList':
        debug("DayList.fromdict() constructor missing")
        

    def insert(self, new_todo: OccasionalTodo):
        if new_todo.day not in self.__daylist:
            self.__daylist[new_todo.day] = [new_todo]
        else:
            self.__daylist[new_todo.day].append(new_todo)

    def remove_todo(self, day: int, *, task: str = None, index: int = None) -> Optional[OccasionalTodo]:
        if task is not None:
            index, todo = self.find_in_day(day, task)
            if todo:
                del self.__daylist[day][index]
                return todo
        elif index is not None:
            if day not in self.__daylist:
                yellow(f"Warning: the day {day} is empty")
            elif index < len(self.__daylist[day]):
                todo = self.__daylist[day][index]
                del self.__daylist[day][index]
                return todo
        else:
            raise ValueError(f"{stack()[0][3]} requires at least one of two optional parameters 'task' and 'index'")
        return None

    def remove_day(self, day: int) -> Optional[List[OccasionalTodo]]:
        if day not in self.__daylist:
            yellow(f"Warning: the day {day} is empty")
        else:
            daylist = self.__daylist[day]
            del self.__daylist[day]
            return daylist
        return None

    def get_day(self, day: int) -> List[OccasionalTodo]:
        if day not in self.__daylist and 0 < day < 367:
            raise EmptyDayException(day)
        return self.__daylist[day]

    def find_in_day(self, day: int, task: str) -> Tuple[Optional[int], Optional[OccasionalTodo]]:
        if day not in self.__daylist:
            yellow(f"Warning: the day {day} is empty")
        else:
            for i, todo in enumerate(self.__daylist[day]):
                if todo.task == task:
                    return i, todo
        return None, None

    def change_day(self, day: int, task: str, new_day: int) -> Optional[OccasionalTodo]:
        index, todo = self.find_in_day(day, task)
        if todo:
            del self.__daylist[day][index]
            todo.day = new_day
            self.insert(todo)
            return todo
        return None

    def __str__(self):
        return str(self.__daylist)

    def __repr__(self):
        return str(self)
