import sys, os
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
import ntpath
from shutil import move
from switch import *
from termcolor import colored

def usage() -> None:
    print('\nUsage:\n\tmvmul [...files] [destination]\n')

def edit() -> None:
    os.system(f"atom {__file__}")

def path_leaf(path:str, get_tail:bool=True) -> str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head) if get_tail else head

def full_path(relative_path:str) -> str:
    home = os.path.expanduser('~')
    return os.path.abspath(relative_path).replace(home, '~')

def move_menu(argv:list) -> None:
    cyan = lambda text: colored(text, 'cyan')
    bold_cyan = lambda text: colored(text, 'cyan', attrs=['bold'])
    bold = lambda text: colored(text, attrs=['bold'])
    max_results = lambda results: max([len(_tup[0]) for _tup in results])

    cardinality = "il file" if len(argv[1:]) == 2 else "i files"
    req = f"\n{cyan(full_path(argv[-1]))} è la cartella in cui vuoi spostare {cardinality} (y/n)? "
    if input(req).lower() == 'y':
        destination = argv[-1] + '/'
        results = []
        for file in argv[1:-1]:
            file_head, file_tail = ntpath.split(file)
            new_path = destination + file_tail
            move(file, new_path)
            dest_start, dest_end = ntpath.split(full_path(new_path))
            results.append((f"{file_head or '.'}/{bold(file_tail)}", f"{bold_cyan('->')} {dest_start}/{bold(dest_end)}"))
        m = max_results(results)
        print()
        for start, end in results:
            print(f"%-{m}s %s\n" % (start, end))

def main(argv:list) -> None:
    with Switch(argv[1]) as s:
        s.case("--edit", edit)
        s.case("-i", usage)
        s.default(move_menu, argv)

if __name__ == '__main__':
    main(sys.argv)
