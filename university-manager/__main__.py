import os
import sys
from typing import List
from src.appunti import appunti
from src.count_lessons import count_lessons
from src.customv import customv
from src.globals import LOG
from src.notes import Notes
from src.rename_recordings import rename_recordings
from src.today_lessons_extractor import Extractor
from switch import Switch
from utils import get_parent_dir, indent_lines
from colors import cyan
from pyerrors import F01, F00

def edit() -> None:
    os.system(f"atom '{get_parent_dir(__file__)}'")


def usage(indentation: int = 0) -> str:
    usage = '\n'
    usage += ''
    usage += '\n'
    return indent_lines(usage, indentation)


def UnknownFlagError(flag: str) -> None:
    raise F01(flag + usage(1))


def test():
    print('hello')


def main(argv: List[str]) -> None:
    min_args = 2
    argv = [*argv, *([''] * (min_args - len(argv) + 1))]
    try:
        with Switch(argv[1]) as s:
            s.exit_case('--edit', edit)
            s.case('-a', appunti, *argv[2:])
            s.case('-c', count_lessons, argv[2] == 'show' if len(argv) == 3 else False)
            s.case('-m', customv, *argv[2:])
            s.case('-r', rename_recordings, *argv[2:4])
            s.case('-s', Notes(argv[2]).split)
            s.case('-j', Notes(argv[2]).join)
            s.case('-tl', Extractor([
                "architettura degli elaboratori", "analisi II",
                "diritto dell'informatica e delle comunicazioni",
                "calcolo numerico", "ingegneria del software"
            ], 3).extract)
            s.case('--test', test)
            s.default(UnknownFlagError, argv[1])
    except IndexError as e:
        raise F00(usage(1))
    except KeyboardInterrupt:
        LOG.write("KeyboardInterrupt")
        pass


if __name__ == '__main__':
    main(sys.argv)
    cyan("Esecuzione terminata\n")
