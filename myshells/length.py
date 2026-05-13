import os, sys
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import *
from piping import get_pipe
from debug import debug

def edit() -> None:
    os.system(f"atom {__file__}")

def main(argv: list) -> None:
    if len(argv) == 1:
        pipe = get_pipe()
        debug(pipe)
        argv.extend(pipe)
    with Switch(argv[1]) as s:
        s.exit_case('--edit', edit)
        s.default(lambda s: print(f'"{s}" is made of {len(s)} characters'), ' '.join(argv[1:]))

if __name__ == '__main__':
    main(sys.argv)
