import os
import sys
from datetime import datetime
from os.path import join, exists
from shutil import copy2

from colors import c_yellow, cyan, c_cyan, red
from debug import debug
from menu import Menu
from src.functions import get_package, get_videos, feature
from src.globals import LOG
from utils import confirm


def get_week_matrix(schedule: dict) -> list:
    # 𝚯(1), anche se più precisamente sarebbe O(day * hours * lesson) = O(day^3),
    # ma fin tanto che day resta illimitato, cosa ovvia per giunta, il costo
    # resta 𝚯(1) mario
    matrix = []
    for day, hours in schedule.items():  # 𝚯(days) = 𝚯(1), days < 6
        if hours:  # 𝚯(1)*𝚯(1) = 𝚯(1)
            matrix.append({})
            for hour, lessons in hours.items():  # 𝚯(hours) = 𝚯(1), hours < 5
                for lesson in lessons:  # 𝚯(lesson) = 𝚯(1), lessons < 3
                    currentDay = matrix[-1]
                    if lesson not in currentDay:
                        currentDay[lesson] = 1
                    else:
                        currentDay[lesson] += 1
    return matrix


def gui_open(file):
    # 𝚯(1)
    if sys.platform == 'win32':
        os.system(f'"{file}"')
    elif sys.platform == 'darwin':
        os.system(f'open "{file}"')


def try_frequency(same_hour_lessons: tuple, frequency: dict) -> int:
    # 𝚯(1)
    left, right = same_hour_lessons
    lf = frequency[left]
    rf = frequency[right]
    if not (lf or rf) or (lf and rf):
        return None
    if lf:
        frequency[left] -= 1
        return 1
    frequency[right] -= 1
    return 2


def get_lesson(schedule: dict, video_title: str, video_path: str, day: int, start_hour: str, frequency: dict) -> str:
    # 𝚯(1)
    def unknown_lesson(open=True):
        lessons = get_package()['folders'].keys()
        lessons = filter(lambda l:l.lower() != 'test' and not l.startswith('_'), lessons)
        intro_message = f'Purtroppo non riesco a capire a quale materia appartiene la lezione {video_title}, puoi selezionare la materia?'
        menu = Menu('Lezione sconosciuta', intro_message=intro_message, return_value=True)
        if open:
            gui_open(video_path)
        for lesson in lessons:
            menu.add_item(lesson, lesson)
        while True:
            lesson = menu.start()
            if lesson is None:
                if confirm('Sei sicuro di voler saltare questa lezione', c_yellow):
                    return None
            else:
                if confirm(f'Confermi che la lezione {video_title} è una lezione di {lesson}', c_yellow):
                    return lesson

    days = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato']
    try:
        schedule[days[day]][start_hour]
    except KeyError:
        start_hour = str(int(start_hour) + 1)
    except Exception as e:
        debug(e)
        return None
    try:
        lessons = schedule[days[day]][start_hour]
    except KeyError:
        return unknown_lesson()
    except Exception as e:
        print(e)
        debug({'start hour': start_hour, 'day': day, 'days[day]': days[day], 'video title': video_title,
               'schedule[days[day]]': schedule[days[day]]})
        exit(1)
    if len(lessons) == 1:
        frequency[lessons[0]] -= 1
        return lessons[0]
    lesson = try_frequency(lessons, frequency)  # 𝚯(1)
    if lesson is None:
        gui_open(video_path)  # 𝚯(1)
        lesson = int(input(
            f"La lezione {c_yellow(video_title)} delle ore {c_yellow(start_hour)} era una lezione di:\n1. {lessons[0]}\n2. {lessons[1]}\n3. Altro...\n> "))
        if lesson == 3:
            return unknown_lesson(open=False)
        frequency[lessons[lesson - 1]] -= 1
    return lessons[lesson - 1]


def add_already_existing(folder: str) -> list:
    # O(videos in folder)
    rgx = r'^([a-zA-Z\s]+)\s\d{1,2}-\d{1,2}-\d{2}(\s\(\d+\))?\.(mp4|mkv)$'
    videos = get_videos(folder, rgx)  # O(videos in folder)
    res = list()
    for video in videos:  # O(videos in folder)
        title, (lesson, _, __) = video
        res.append((lesson, join(folder, title), title))
    return res


def rename_recordings(folder: str, destination: str) -> None:
    # O(n), n = number of videos in folder
    feature("Rename Recordings")
    LOG.newline()

    package = get_package()  # 𝚯(1)

    schedule = package['schedule']
    folders = package['folders']
    week_matrix = get_week_matrix(schedule)  # 𝚯(1)

    videos = get_videos(folder)  # O(videos in folder)
    renamed = list()

    for video in videos:  # O(videos in folder)
        video_title, (date, hour, ext) = video
        old_path = join(folder, video_title)

        date = date.split('-')
        hour = str(int(hour.split('-')[0]))
        # str-int serve a togliere un eventuale 0 iniziale

        wday = int(datetime(*map(int, date)).strftime('%w'))
        frequency = week_matrix[wday - 1]

        date.reverse()
        date[2] = date[2][2:]
        date = '-'.join(date)

        lesson = get_lesson(schedule, video_title, old_path, wday, hour, frequency)  # 𝚯(1)

        if lesson:
            new_title = f'{lesson} {date}.{ext}'
            new_path = join(folder, new_title)
            i = 2
            while exists(new_path):  # 𝚯(n video già esistenti con stesso titolo), ma generalmente è solo 𝚯(1)
                new_path = join(folder, f'{lesson} {date} ({i}).{ext}')
                i += 1
            cyan(f"\nRinomino {c_yellow(old_path)} {c_cyan('in')} {c_yellow(new_path)}\n")
            LOG.write(f"Rinomino {old_path} in {new_path}")
            try:
                os.rename(old_path, new_path)
                renamed.append((lesson, new_path, new_title))
            except Exception as e:
                LOG.write(str(e.with_traceback()))
                raise e

    for video in add_already_existing(folder):  # O(videos in folder)
        if not video in renamed:
            renamed.append(video)

    for video in renamed:  # O(videos in folder), renamed <= folder
        lesson, old_path, title = video
        dst = join(destination, folders[lesson], folders["_lessons"])
        new_path = join(dst, title)
        sys.stdout.write(f"{c_cyan('Copio')} {c_yellow(title)} {c_cyan('in')} {c_yellow(dst)}...")
        sys.stdout.flush()
        if not exists(new_path):
            copy2(old_path, new_path)
            print('OK\n')
            LOG.write(f"Copio {title} in {dst}")
        else:
            red("ALREADY EXISTS\n")
            LOG.write(f"Non ho potuto copiare {title} in {dst} perché esisteva già")