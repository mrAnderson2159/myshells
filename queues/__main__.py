from src.database import Database
from src.menu import MainMenu
import os,sys
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from utils import indent_lines, get_parent_dir, clear
from pyerrors import *

def edit() -> None:
    os.system(f"atom '{get_parent_dir(__file__)}'")

def usage(indentation:int = 0) -> str:
    usage = '\n'
    usage += ''
    usage += '\n'
    return indent_lines(usage, indentation)

def run():
    database = Database(f'{get_parent_dir(__file__)}/src/database.json')
    menu = MainMenu("Menù principale", database)

    menu()
    clear()

def UnknownFlagError(flag:str) -> None:
    raise F01(flag + usage(1))

def main(argv: List[str]) -> None:
    if len(argv) == 1:
        argv.append('')
    try:
        with Switch(argv[1]) as s:
            s.exit_case('--edit', edit)
            s.case('', run)
            s.default(UnknownFlagError, argv[1])
    except IndexError:
        raise F00(usage(1))
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main(sys.argv)
