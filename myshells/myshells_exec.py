import os, sys, platform, shutil, re
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from pathlib import Path
from switch import *
from pyerrors import *
from utils import *
from debug import *
from typing import List
from paths import *


sep = sep()
home = home()
plat = plat()
myshells = myshells_path()
bash_profile = str()

with Switch(plat) as s:
    def mod(name:str):
        global bash_profile
        bash_profile = name
    def NotImplementedOsError(os_name:str) -> None:
        raise O00(os_name)
    s.case('Windows', mod, '.bashrc')
    s.case('Darwin', mod, '.zshenv')
    s.case('Linux', NotImplementedOsError, plat)
    s.case('CYGWIN_NT-10.0-19043', mod, '.zshrc')
    s.default(NotImplementedOsError, plat)

    bash_profile = home + bash_profile

def edit() -> None:
    os.system(f"atom {__file__}")

def rechargeOSXconsole(command:str) -> None:
    with open(f"{home}/.zsh_history", 'a') as h:
        h.write('\n'+command)
    os.system('/bin/zsh')

def usage(indentation:int = 0) -> str:
    usage = '\nusage: myshells [-i-cd-mk] [filename [,aliasname]]'
    usage += '\n\t-i: get infos'
    usage += '\n\t-mk: move new shell inside myshells, create an alias '
    usage += f'and source {bash_profile}; \n\t     file\'s name and optionally alias name '
    usage += '[file\'s name will be used as alias name by default]\n'
    return indent_lines(usage, indentation)

def make_shell(argv:List[str]) -> None:
    [path, [filename, extention]] = [argv[2], os.path.splitext(argv[2])] #ottengo il percorso del file, il percorso del file senza estensione e l'estensione
    filename = filename.split(sep)[-1] # ottengo il nome del file
    try:
        with Switch(extention) as s:
            env = str()
            def mod(env_name:str) -> None:
                nonlocal env
                env = env_name
            def NotImplementedExtentionError(extension:str) -> None:
                raise E00(extension)
            s.case('.py', mod, 'python3')
            s.case('.js', mod, 'node')
            s.default(NotImplementedExtentionError, extention)
    except Exception as e:
        print("Non riconosco l'estensione, in che linguggio è scritto il programma?")
        env = ['python3', 'node'][int(input('\t1. python\n\t2. javascript\n> ')) - 1]

    alias = argv[3] if len(argv) == 4 else filename # creo l'alias che sarà il nome del file o un alias fornito come ultimo argomento dall'utente
    ms_file_path = myshells + filename + extention
    shutil.copy(path, ms_file_path)
    os.remove(path)
    with open(bash_profile, 'a') as bp:
        bp.write(f"\nalias {alias}='{env} \"{ms_file_path}\"'")
    with open(bash_profile, 'r') as bp:
        last3lines = bp.read().split('\n')[-3:]
        print('.\n'*3, end='')
        [print(line) for line in last3lines]
    if plat == 'Darwin':
        rechargeOSXconsole(f'myshells -mk {path} {alias}')

def UnknownFlagError(flag:str) -> None:
    raise F01(flag + usage(1))

def cd() -> None:
    if plat == 'Darwin' or re.match(r'^CYGWIN_NT', plat):
        os.chdir(myshells)
        rechargeOSXconsole(f'cd {myshells}')
    else:
        raise T00(plat)

def main(argv: List[str]) -> None:
    if len(argv) == 1:
        raise F00(usage(1))
    with Switch(argv[1]) as s:
        s.exit_case('--edit', edit)
        s.case('-i', print, usage())
        s.case('-cd', cd)
        s.case('-mk', make_shell, argv)
        s.default(UnknownFlagError, argv[1])

if __name__ == '__main__':
    main(sys.argv)
