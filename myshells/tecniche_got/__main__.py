import os, sys, re, json
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import *
from utils import get_parent_dir
from termcolor import colored
from colors import cyan

this = get_parent_dir(__file__)
db = this + "tecslist.json"

def edit() -> None:
    os.system(f"atom {this}")

def diff(old:list, new:list) -> tuple:
    red = lambda s: colored('>> ' + s, 'red')
    green = lambda s: colored('<< ' + s, 'green')
    old = set(old)
    new = set(new)
    outgoing = old - new
    incoming = new - old
    result = list(map(red, outgoing))
    result.extend(list(map(green, incoming)))
    return (result, len(outgoing))

def db_write(tecslist:str) -> None:
    with open(db, "w") as f:
        f.write(json.dumps(tecslist))
        print("I cambiamenti sono stati salvati")

def print_join(_list:list, join:str='\n', prepend='') -> None:
    print(end=prepend)
    print(join.join(_list))

def save(tecslist:list) -> None:
    try:
        with open(db, "r") as f:
            prev_tecslist = json.loads(f.read())
            differences, elementsWhereRemoved = diff(prev_tecslist, tecslist)
            if elementsWhereRemoved:
                print("Confermi di voler salvare i seguenti cambiamenti? (y/n)")
                print_join(differences)
                if input('> ').lower() == 'y':
                    db_write(tecslist)
            else:
                db_write(tecslist)
    except FileNotFoundError:
        db_write(tecslist)


def load(tecslist:list) -> None:
    with open(db, "r+") as f:
        prev_tecslist = json.loads(f.read())
        [tecslist.append(tec) for tec in prev_tecslist if not tec in tecslist]

def print_tecslist(tecslist:list) -> None:
    print_join(tecslist, '\n\t', '\t')

def option(name:str, value:bool) -> callable:
    def decorator(function: callable) -> callable:
        def inner(*args, **kwargs):
            function(*args, **kwargs)
            print(f"L'opzione {name} è stata {'attivata' if value else 'disattivata'}")
        return inner
    return decorator

@option("autoprint", False)
def disable_autoprint(options:dict) -> None:
    options["autoprint"] = False

@option("autoprint", True)
def enable_autoprint(options:dict) -> None:
    options["autoprint"] = True

def print_options(options:dict) -> None:
    print("{")
    [print(f"\t{key}: {value}") for key, value in options.items()]
    print("}")

def print_commands(commands: list):
    print_join(commands, '\n\t', '\t')

def clear():
    os.system('clear')
    print("Inserisci un comando")

def exec_command(command: str, current_list: list, options: dict) -> None:
    if not re.search(r"\s",command):
        command += ' '
    command, body = command.split(' ', 1)
    with Switch(command) as s:
        s.case("shift", lambda: current_list.pop(0))
        s.case("pop", lambda: current_list.pop())
        s.case("unshift", lambda: current_list.insert(0, body))
        s.case("push", lambda: current_list.append(body))
        s.case("save", save, current_list)
        s.case("load", load, current_list)
        s.case("print", print_tecslist, current_list)
        s.case("disable_autoprint", disable_autoprint, options)
        s.case("enable_autoprint", enable_autoprint, options)
        s.case("options", print_options, options)
        s.case("clear", clear)
        s.case("help", print_commands, s._cases)
        if command in ('unshift','shift','pop', 'push', 'load') and options["autoprint"]:
            print_tecslist(current_list)

def default() -> None:
    os.system('clear')
    load(tecslist := list())
    options = {
        "autoprint": True
    }
    print("Tecniche da apprendere:")
    print_tecslist(tecslist)
    print("\nInserisci un comando")
    while True:
        command = input("> \x1b[93m")
        if command in ('esci', 'exit'):
            break
        print('\x1b[0m', end='')
        exec_command(command, tecslist, options)

def main(argv: list) -> None:
    if len(argv) == 1:
        argv.append('')
    try:
        with Switch(argv[1]) as s:
            s.exit_case('--edit', edit)
            s.default(default)
    except KeyboardInterrupt:
        cyan("\n\nEsecuzione terminata\n")

if __name__ == '__main__':
    main(sys.argv)
