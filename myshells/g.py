import os, sys, re
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import *
from os.path import isfile, splitext

def verify_argv(argv: list) -> AssertionError:
    if len(argv) == 2 and argv[1] == '--edit':
        return
    argumentsError = "this program takes at least 2 arguments: a flag and a filename"
    assert len(argv) >= 3, argumentsError

def raise_wrong_flag_error() -> ValueError:
    allowedFlags = lambda : ', '.join(['-c', '-cpp'])
    wrongFlagError = f"this flag is unknown, use {allowedFlags()}"
    raise ValueError(wrongFlagError)

def raise_main_missing_error() -> ValueError:
    mainMissingError = 'Missing indications about the main file. The main file must whether be called\
                      \nmain.c or must be explicitly indicated as main=main_file.c'
    raise ValueError(mainMissingError)

def edit():
    os.system(f"atom {__file__}")
    exit(0)

def get_flags(_list: list) -> str:
    return " ".join([flag for flag in _list if flag[0] == '-'])

def get_option_argument(option: str) -> str:
    split_option = option.split('=')
    return split_option[1] if len(split_option) == 2 else split_option[0]

def get_file(_list: list) -> str:
    return splitext([el for el in _list if isfile(el)][0])[0]

def get_files(_list: list) -> list:
    return [splitext(f)[0] for f in _list[2:] if isfile(get_option_argument(f))]

def get_files_without_options(_list: list) -> list:
    return [get_option_argument(file) for file in _list]

def get_main_file(files: list) -> str:
    if not 'main' in files:
        containing_main = [name for name in files if re.match(r'main=',name)]
        if not len(containing_main):
            raise_main_missing_error()
        return containing_main[0][5:]
    else:
        return 'main'

def c(argv: list) -> None:
    flags = get_flags(argv[2:])
    filename = get_file(argv[2:])
    os.system(f"gcc -o {flags} {filename} {filename}.c; ./{filename}")

def cpp(argv: list) -> None:
    flags = get_flags(argv[2:])
    filename = get_file(argv[2:])
    os.system(f"g++ -Wall -pedantic -std=c++17 -o {flags} {filename} {filename}.cpp; ./{filename}")

def cm(argv: list) -> None:
    files = get_files(argv)
    main_file = get_main_file(files)
    files = get_files_without_options(files)

    base_command = f'gcc -c {get_flags(argv[2:])}'
    final_command = ''

    for file in files:
        final_command += f"{base_command} {file}.c; "
    final_command += f"rm {main_file}; gcc -o {main_file} {' '.join([file+'.o' for file in files])}; ./{main_file}"
    os.system(final_command)

def main(argv):
    verify_argv(argv)
    flag = argv[1]

    with Switch(flag) as s:
        s.case('--edit', edit)
        s.case('-c', c, argv)
        s.case('-cpp', cpp, argv)
        s.case('-cm', cm, argv)
        s.default(raise_wrong_flag_error)

if __name__ == '__main__':
    main(sys.argv)
