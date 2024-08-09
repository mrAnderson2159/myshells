import os, sys, re
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from debug import debug
from pyerrors import *

def get_full_path(arg:str) -> str:
    if os.path.exists(arg):
        path = os.path.realpath(arg)
        if path.split('/')[1] == 'NAS4A1AB2':
            path = '/'+path

        if re.search(r"/cygdrive/c", path):
            path = path.replace("/cygdrive/c", "C:\\").replace("/", "\\")

        return f'"{path}"'
    else:
        return arg

if __name__ == '__main__':
    args = sys.argv[1:]
    if not len(args):
        raise A00("Questo file richiede almeno un argomento")

    if args[0] == '--edit':
        os.system(f'atom "{__file__}"')
        exit(0)

    realpath_args = map(get_full_path, args)
    str_args = ' '.join(realpath_args)
    os.system(str_args)
