import sys
import os
from pathlib import Path

def usage():
    s = "\nUsage: cdmkdir [, -i, -o, --options=mkdir_options] [new folder name]:"
    s += "\n\t-i: print info\n\t-o: open folder in GUI after creation"
    s += "\n\t--options=mkdir_options: add flags to mkdir command\n"
    print(s)

if len(sys.argv) < 2:
    print(f"\nError: cdmkdir takes at least 1 positional parameter, {len(sys.argv) - 1} recieved")
    usage()
    sys.exit(1)

home = str(Path.home()) # ~
flag = sys.argv[1]

def mkdir(argvPoint = 1, callback = lambda : None, options = ''):
    dir = '\ '.join(map(lambda x : '\ '.join(x.split(' ')), sys.argv[argvPoint:])) # escape
    os.system(f"mkdir {options} {dir}")
    os.chdir(dir.replace('\\', '')) # imposta la cartella di ambiente sulla nuova appena creata
    os.system(f"echo \"cdmkdir {' '.join(sys.argv[1:])}\" >> {home}/.zsh_history") # aggiorna la cronologia
    callback()
    os.system("/bin/zsh") # ricarica la console

if flag == '--edit':
    os.system(f"atom {__file__}")
elif flag == '-o':
    mkdir(2, lambda : os.system(f"open ."))
elif flag == '-i':
    usage()
elif flag[:11] == '--options=-':
    mkdir(2, options = flag[10:])
else:
    mkdir()
