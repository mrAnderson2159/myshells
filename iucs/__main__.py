import os, sys
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import Switch
from debug import debug
from piping import get_pipe
from utils import *
from inspect import getframeinfo, stack
from termcolor import colored

def print_color(color):
    def init(string, **kwargs):
        print(colored(string, color), **kwargs)
    return init

cyan = print_color('cyan')
green = print_color('green')
yellow = print_color('yellow')
red = print_color('red')
this_dir = get_parent_dir(__file__, with_slash=False)

def edit() -> None:
    os.system(f"atom {this_dir}")

def _e(e:str) -> str:
    class E:
        def __init__(self, name, msg):
            self.name = name
            self.msg = msg

        def __str__(self):
            return self.msg

    return {
        'm_p': E(
            name='missing parameter',
            msg="Non sono stati inseriti abbastanza parametri per questa funzione."
            ),
        'n_e_f': E(
            name='not empty file',
            msg="Il portale contiene ancora dei dati e non può essere sovrascritto. Leggere i dati quindi scriverne di nuovi."
            ),
        'd_e_y': E(
            name="does not exist yet",
            msg="Il portale non è ancora stato creato"
            )
    }[e]

def _r(f:str) -> str:
    _ = {
        '-c': ['nuovo percorso']
    }
    _['--change-path'] = _['-c']
    return _[f]

def _confirms():
    return 'y','Y','yes','Yes','YES'

def _from_b(data:str) -> str:
    data = data.split('\n')
    data = map(lambda s:''.join([chr(int(f'0x{b}',16)) for b in s.split(' ') if b]), data)
    return '\n'.join(data)

def _to_b(data:str) -> str:
    return ' '.join([str(hex(ord(c)))[2:] for c in data])

def _read_path() -> str:
    with open(f"{this_dir}/PATH.dat", 'r') as f:
        res = f.read()
        return _from_b(res)

def _extend_argv(argv, required_args):
    pipe = get_pipe()
    if len(pipe):
        argv.extend(pipe)
    else:
        for i in range(required_args):
            argv.append('')

def _delimiter():
    return '\n'*3+'-'*10+'\n'

def change_path(new_path:str) -> bool:
    if input(f"Sicuro di voler cambiare il percorso in {new_path}? Questo processo è pericolo e va eseguito da entrambe le parti per non compromettere il funzionamento del programma (y/n): ") in _confirms():
        try:
            with open(f"{this_dir}/PATH.dat", 'w') as f:
                f.write(_to_b(new_path))
            return True
        except Exception as e:
            print(e.with_traceback())
            return False

def read() -> None:
    path = _read_path()
    try:
        with open(path, 'r') as f:
            data = _from_b(f.read())
            sys.stdout.write(data)
    except FileNotFoundError:
        print(_e('d_e_y'))
    with open(path, 'w') as f:
        f.write('')

def write(data: str) -> bool:
    path = _read_path()
    try:
        with open(path, 'r') as f:
            if _from_b(f.read()):
                print(_e('n_e_f'))
                return False
    except FileNotFoundError:
        pass
    with open(path, 'w') as f:
        f.write(_to_b(data))
        f.write(_to_b(_delimiter()))
        return True

def append(data: str) -> None:
    path = _read_path()
    with open(path, 'a') as f:
        f.write('\n'+_to_b(data))
        f.write(_to_b(_delimiter()))
        return True

def main(argv: list) -> None:
    flag = argv[1]
    required_args = 1
    _extend_argv(argv, required_args)
    with Switch(flag) as s:
        s.exit_case('--edit', edit)
        s.case(('-r','--read'), read)
        s.case(('-c', '--change-path'), change_path, argv[2])
        s.case(('-w','--write'), write, ' '.join(argv[2:]))
        s.case(('-a','--append','--add'), append, ' '.join(argv[2:]))

if __name__ == '__main__':
    main(sys.argv)
    _read_path()
