import sys, os
from os.path import join
from pathlib import Path

def get_alias(alias):
    bash_profile_position = join(Path().home(), '.zshenv')
    with open(bash_profile_position, 'r') as bp:
        aliases = filter(lambda a: a[:5] == 'alias' ,bp.readlines())
        aliases = list(map(lambda a: a[6:].split('=', 1), aliases))
        try:
            return {key: value[1:-2] for key, value in aliases}[alias]
        except KeyError:
            return alias

if len(sys.argv) < 2:
    pipe = sys.stdin.read()[:-1]
    os.system(f"echo \"{pipe}\" | tr -d \"\\n\"| pbcopy")

elif sys.argv[1] == "--edit":
    os.system(f"atom {__file__}")
    sys.exit(0)

else:
    os.system(f"{' '.join(map(get_alias, sys.argv[1:]))} | python {__file__}")
