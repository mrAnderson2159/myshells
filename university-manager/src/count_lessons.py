import sys
from os.path import join

from termcolor import colored

from colors import cyan, c_cyan, c_green, c_yellow, c_red, c_blue, c_white
from src.functions import feature, get_package, get_videos, get_tag
from src.globals import LOG


def print_from_tag(show: bool, counter: dict, tags: list, priority: str, tag_name: str, counter_field: str):
    if tag_name in tags:
        total = len(tags[tag_name])
        print(colored(f'\t{priority} ({total}){":" if show else ""}', tag_name if tag_name != 'none' else 'white'))
        counter[counter_field] += total
        if show:
            for tag in tags[tag_name]:
                print(f'\t\t{tag}')
            print()


def count_lessons(show: bool) -> None:
    feature("Count Lessons")

    if sys.platform != 'darwin':
        raise OSError("Questo programma funziona soltanto su mac")

    package = get_package()
    lessons = [(key, value) for key, value in package['folders'].items() if not key.startswith('_') and key != 'Test']
    university = package["paths"]["università"]["darwin"]
    paths = list(map(lambda l: join(university, l[1], package['folders']['_lessons']), lessons))

    rgx = r'^([a-zA-Z\s]+)\s\d{1,2}-\d{1,2}-\d{2}(\s\(\d+\))?\.(mp4|mkv)$'

    counter = {f'_{w}': 0 for w in ("total", "done", "loading", "todo", "todo_later", "unknown")}

    print_tags = [
        ('Da fare', 'red', '_todo'),
        ('Da fare ma dopo l\'esame', 'blue', '_todo_later'),
        ('In corso', 'yellow', '_loading'),
        ('Completate', 'green', '_done'),
        ('Dati non disponibili', 'none', '_unknown')
    ]

    for path, lesson in zip(paths, map(lambda l: l[0], lessons)):
        videos = list(map(lambda v: v[0], get_videos(path, rgx)))
        tags = [get_tag(join(path, v)) for v in videos]
        counter[lesson] = {tag: list() for tag in set(tags)}
        counter[lesson]["_total"] = 0
        for video, tag in zip(videos, tags):
            counter[lesson][tag].append(video)
            counter[lesson]["_total"] += 1
            counter["_total"] += 1
        tags = counter[lesson]
        cyan(f'{lesson} ({tags["_total"]}):')
        for print_tag in print_tags:
            print_from_tag(show, counter, tags, *print_tag)

    LOG.newline()

    # def output_message(colors:List[Callable[[str], str]]=None) -> str:
    #     strings = ("In totale le lezioni sono {total} di cui",
    #                 "{done} completate",
    #                 "{loading} in corso",
    #                 "{todo} da fare",
    #                 "{todo_later} da fare dopo l'esame",
    #                 "{unknown} i cui dati non sono disponibili"
    #         )
    #     attrs = ['total', 'done', 'loading', 'todo', 'todo_later', 'unknown']
    #
    #     def msg() -> str:
    #         res = []
    #         for i, string in enumerate(strings):
    #             if counter['_'+attrs[i]]:
    #                 value = '_' + attrs[i]
    #
    #                 res.append(str.format(string, value=colors[i](counter[value])))
    #         return clever_join(res, ', ', ' e ')
    #
    #     if colors is None:
    #         colors = [lambda s: s] * len(strings)
    #
    #     else:
    #         assert len(colors) == len(strings)
    #     return msg()

    print(
        f"\nIn totale le lezioni sono {c_cyan(counter['_total'])} di cui "
        f"{c_green(counter['_done'])} completate, {c_yellow(counter['_loading'])} in corso, "
        f"{c_red(counter['_todo'])} da fare, {c_blue(counter['_todo_later'])} da fare dopo l'esame e "
        f"{c_white(counter['_unknown'])} i cui dati non sono disponibili.\n")
    #print(output_message([c_cyan, c_green, c_yellow, c_red, c_blue, c_white]))
    LOG.write(
        f"In totale le lezioni sono {counter['_total']} di cui {counter['_done']} completate, "
        f"{counter['_loading']} in corso, {counter['_todo']} da fare, "
        f"{counter['_todo_later']} da fare dopo l'esame e "
        f"{counter['_unknown']} i cui dati non sono disponibili.\n")