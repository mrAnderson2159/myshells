import os, sys, platform, re
from pathlib import Path
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
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
    if isMac():
        bashprofile = '.zshenv'
    elif isCyg():
        bashprofile = '.zshrc'
    else:
        raise O00(f"Function not implemented for {plat()} yet. Sorry...")
    return os.path.realpath(home()+bashprofile)

def thisname(filename:str) -> str:
    return os.path.splitext(filename)[0].split(sep())[-1]
