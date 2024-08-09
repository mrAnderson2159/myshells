import os, sys
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import *

def edit() -> None:
    os.system(f"atom {__file__}")

def move(filename: str) -> None:
    PATH = "/Users/mr.anderson2159/Documents/My\\ Music/sheet\\ music"
    os.system(f"mv {filename} {PATH}")
    print(f"{filename} moved to {PATH}")

def main(argv: list) -> None:
    with Switch(argv[1]) as s:
        s.exit_case('--edit', edit)
        s.case('-m', move, argv[2])

if __name__ == '__main__':
    main(sys.argv)
