import os
import sys
import platform
import re
import subprocess
from pathlib import Path
from pyerrors import *

def isMac() -> bool:
    return plat() == 'Darwin'

def isCyg() -> bool:
    return bool(re.match(r'^CYGWIN_NT', plat()))

def isWin() -> bool:
    return plat() == 'Windows'

def sep() -> str:
    return os.path.sep

def home() -> str:
    return str(Path.home()) + sep()

def plat() -> str:
    return platform.system()

def myshells_path() -> str:
    return ('/' if isCyg() or isWin() else '') + os.path.realpath(home() + 'myshells') + sep()

def working_space_path() -> str:
    return ('/' if isCyg() or isWin() else '') + os.path.realpath(home() + 'working space') + sep()

def bash_profile() -> str:
    shell_path = subprocess.run('echo $SHELL', shell=True, capture_output=True, text=True).stdout.strip()
    shell_name = Path(shell_path).name

    bash_profile = ''

    match shell_name:
        case 'zsh':
            bash_profile = '.zshenv'
        case 'bash':
            bash_profile = '.bash_profile'
        case _:
            raise O00(f"Function not implemented for {shell_name} or {plat()} yet. Sorry...")

    return os.path.realpath(home() + bash_profile)

def thisname(filename:str) -> str:
    return os.path.splitext(filename)[0].split(sep())[-1]
