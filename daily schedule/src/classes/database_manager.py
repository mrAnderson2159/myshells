from pathlib import Path
from typing import Union, List, Dict
from json import dumps, loads
from os.path import exists

from src.classes.fixed_todo import FixedTodo
from src.classes.day_list import DayList


class DatabaseManager:
    def __init__(self, database_path: Union[str, Path]):
        if not exists(database_path):
            with open(database_path, 'w') as file:
                file.write(dumps({
                    "todo": {
                        "fixed": {},
                        "occasional": {}
                    }
                }))
            self.database = dict()
        else:
            with open(database_path, 'r') as file:
                self.database: dict = loads(file.read())

    def get_fixed(self) -> List[List[FixedTodo]]:
        fixed: Dict[str, dict] = self.database['todo']['fixed']
        result: List[List[FixedTodo]] = [[] for _ in range(7)]

        for todo_dict in fixed.values():
            todo = FixedTodo.fromdict(todo_dict)
            start_day = current_day = todo.day
            repetition = todo.repetition
            ring_index = 0
            module = len(repetition)

            while True:
                current_day += repetition[ring_index]
                current_day %= 7
                result[current_day].append(todo)
                if current_day == start_day:
                    break
                if module > 1:
                    ring_index += 1
                    ring_index %= module

        return result

    def get_occasional(self) -> DayList:
        return DayList.fromdict(self.database['todo']['occasional'])

    def save(self):
        pass

    def update_fixed(self, fixed_list: List[List[FixedTodo]]):
        pass

    def update_occasional(self, occasional_list: DayList):
        pass
