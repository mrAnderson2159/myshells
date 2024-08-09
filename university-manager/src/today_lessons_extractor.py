__all__ = ['Extractor']

from typing import List
from random import randint
from colors import cyan, yellow
from debug import debug
from utils import confirm, clever_join, capitalize
from src.functions import get_package, write_package, get_today, feature


class Extractor:
    def __init__(self, lessons: List[str], daily_lessons: int):
        self.lessons = list(map(capitalize, lessons))
        self.daily_lessons = daily_lessons
        self.today = get_today()

        try:
            self.lesson_extraction: dict = get_package()["lesson_extraction"]

            if len(self.lesson_extraction['available']) + len(self.lesson_extraction['extracted']) < daily_lessons:
                raise Exception("Il numero di lezioni fa fare al giorno è maggiore del numero di lezioni disponibili")

            total_lessons = {*self.lesson_extraction['available'], *self.lesson_extraction['extracted']}
            if total_lessons != set(self.lessons):
                if confirm(f"Le lezioni inserite non corrispondono a quelle presenti nel database, vuoi sostituire "
                           f"{yellow(clever_join(total_lessons, ', ', ' e '))} con "
                           f"{cyan(clever_join(self.lessons, ', ', ' e '))}"):
                    self.__initialize_lesson_extraction()
                else:
                    raise RuntimeError("Il programma non può essere eseguito")

        except KeyError:
            self.__initialize_lesson_extraction()

    def __initialize_lesson_extraction(self):
        self.lesson_extraction = {
            "available": self.lessons,
            "extracted": [],
            "date": None
        }
        self.__write_package()

    def __write_package(self):
        package = get_package()
        package['lesson_extraction'] = self.lesson_extraction
        write_package(package)

    def extract(self):
        feature("Today Lessons Extractor")

        todo = self.lesson_extraction['extracted'][-self.daily_lessons:]
        # debug(self.lesson_extraction['date'], self.today, self.lesson_extraction['date'] != list(self.today))
        if self.lesson_extraction['date'] != self.today:
            available = self.lesson_extraction['available']
            extracted = self.lesson_extraction['extracted']
            todo = []

            def append_lesson(todo: list, extractions: int):
                nonlocal self, available

                for i in range(extractions):
                    index = randint(0, len(available) - 1)
                    lesson = available[index]
                    todo.append(lesson)
                    del self.lesson_extraction['available'][index]
                    self.lesson_extraction['extracted'].append(lesson)

            if len(available) >= self.daily_lessons:
                append_lesson(todo, self.daily_lessons)
            else:
                from_extracted = self.daily_lessons - len(available)
                todo = [*available]
                available = self.lesson_extraction['available'] = [*extracted]
                self.lesson_extraction['extracted'] = [*todo]

                append_lesson(todo, from_extracted)

            self.lesson_extraction['date'] = self.today
            self.__write_package()

        print(f'Le lezioni da fare oggi sono: ')
        for lesson in todo:
            yellow(f'\t{lesson}')
        print()
