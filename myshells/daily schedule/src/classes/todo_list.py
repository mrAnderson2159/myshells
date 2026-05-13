from datetime import datetime, timedelta
from typing import List, Generator, Union, Tuple, Sequence
from pathlib import Path
from os import system

from src.classes.day_list import *
from src.classes.fixed_todo import FixedTodo
from src.classes.occasional_todo import OccasionalTodo
from src.classes.todo import Todo
from src.classes.database_manager import DatabaseManager
from src.interfaces.time import Time
from src.interfaces.printer import Printer


class TodoList(Time, Printer):
    def __init__(self, database_path: Union[str, Path], printer: bool = False):
        self.db_manager = DatabaseManager(database_path)
        self.occasional_list = self.db_manager.get_occasional()
        self.fixed_list = self.db_manager.get_fixed()

        self.today = datetime.now()
        self.wday = self.get_wday(self.today)
        self.yday = self.get_yday(self.today)
        self.year_start = datetime(self.today.year, 1, 1)
        self.last_day_printed: int = 0
        self.printer = printer

    def print_day_list(self, day: int):
        try:
            occasional = self.occasional_list.get_day(day)
        except AttributeError:#EmptyDayException:
            occasional = []

        start = self.year_start
        if self.yday > day:
            start += timedelta(days=365)

        date = start + timedelta(days=day - 1)
        wday = self.get_wday(date)
        fixed = self.fixed_list[wday]

        todos: Generator[Todo] = (todo for todo in (*fixed, *occasional))

        res = self.it_date(date) + '\n\n'

        for todo in todos:
            res += f'- {todo}\n'

        print(res)

        if self.printer:
            self.print_out(res)

    def print_today_list(self):
        self.print_day_list(self.yday)

    def process_repetition(self, repetition: str) -> Tuple[int]:
        return tuple(map(int, repetition.split(' ')))

    def add_fixed(self, task: str, day: int, repetition: Tuple[int]) -> FixedTodo:
        todo = FixedTodo(task, day, repetition)
        self.fixed_list[todo.day].append(todo)
        self.db_manager.update_fixed(self.fixed_list)
        return todo

    def add_occasional(self, task: str, day: int, rep: Tuple[int]) -> OccasionalTodo:
        todo = OccasionalTodo(task, day, rep)
        self.occasional_list.insert(todo)
        self.db_manager.update_occasional(self.occasional_list)
        print(self.occasional_list)
        return todo
    