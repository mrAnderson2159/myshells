import os, sys, re
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import *
from typing import *
from debug import debug
from utils import indent_lines
from pyerrors import *
from colors import *

def edit() -> None:
    os.system(f'open -a "PyCharm CE" "{__file__}"')

def usage(indentation:int = 0) -> str:
    usage =  f'\n{c_green("USAGE")}: sha [-1,-256,-512] [string] [,case,slicinig,step,compose] [,**kwargs]\n\n'
    usage += f'\t{c_cyan("-1, -256, -512")}: ecrypts the string using the selected sha algorithm\n'
    usage += f'\t{c_cyan("string")}: the string to encrypt\n'
    usage += f'\t{c_cyan("case [optional]")}: chose to get the encrypted string in lower (low) or upper (up) case [default: low]\n'
    usage += f'\t{c_cyan("slicinig [optional]")}: slice part of the encryped string [exemple 0:16, :32, 16:, 4:28]\n'
    usage += f'\t{c_cyan("step [optional]")}: jump each n character separating with a space [exemple 4 -> ae45 b6d2 680a 9ef3]\n'
    usage += f'\t{c_cyan("compose [optional]")}: allows to get parts of the encrypted string in upper and lower case\n'
    usage += f'\t\t\t[exemple :16up16:32low32:40up returns a string in lowercase from beginning to 15th character,\n'
    usage += f'\t\t\tin uppercase from 16th character to 31st and lower from 32nd to 40th]\n'
    usage += f'\t{c_cyan("**kwargs")}: you may prefer specifing arguments in whatever argument by passing their name at the beginning [exemple case=low step=4 slice=:16]\n'
    usage += f'\n'
    return indent_lines(usage, indentation)

def process_args(argv:List[str]) -> str:
    argv = [arg for arg in argv if arg]
    if len(argv) < 2:
        raise A00(f"This program needs at least two argument: the sha type algorithm and the string to encrypt, {len(argv)} recieved {usage(1)}")

    sha_type = argv[0]
    string = argv[1]
    case = str.lower
    slicing = None
    step = None
    compose = None

    def process_type():
        nonlocal sha_type
        if not sha_type in ['-1', '-256', '-512']:
            raise A00(f"Sha algorithm must be -1, -256 or -512, not {sha_type}")
        sha_type = sha_type[1:]

    def process_case():
        nonlocal case
        regex = r'^(case=)?(low|up)$'
        for arg in argv:
            match = re.match(regex, arg)
            if match:
                case = str.lower if match.group(2) == 'low' else str.upper
                break

    def process_slicing():
        nonlocal slicing
        regex = r'^((slice|slicing)=)?(-?\d*?):(-?\d*?)$'
        for arg in argv:
            match = re.match(regex, arg)
            if match:
                start = int(match.group(3)) if match.group(3) else None
                stop = int(match.group(4)) if match.group(4) else None
                slicing = start, stop
                break

    def process_step():
        nonlocal step
        regex = r'^(step=)?(\d+)$'
        for arg in argv:
            match = re.match(regex, arg)
            if match:
                step = int(match.group(2))
                break

    def process_compose() -> None:
        class Group:
            def __init__(self, start:int, stop:int, case:str):
                self.start = start
                self.stop = stop
                self.case = case
                self.case_function = str.lower if case == 'low' else str.upper
            def __repr__(self):
                return str((self.start, self.stop, self.case))
        def group(pattern:str) -> Sequence[str]:
            return re.match(r'(-?\d*?):(-?\d*?)([a-z]+)', pattern).groups()
        def type_group(group: Sequence[str]) -> Group:
            ret = lambda index: int(group[index]) if group[index] else None
            return Group(ret(0), ret(1), group[2])
        def match_group(type_group:Iterable[Group])  -> Tuple[Group]:
            type_group = list(type_group)
            for i in range(1, len(type_group)):
                if not type_group[i].start and type_group[i-1].stop:
                    type_group[i].start = type_group[i-1].stop
            return tuple(type_group)

        nonlocal compose
        regex = r'(compose=)?((-?\d*?:-?\d*?)(low|up))+'
        for arg in argv:
            match = re.match(regex, arg)
            if match:
                arg_temp = arg
                res = []
                if match.group(1) == 'compose=':
                    arg_temp = arg[8:]
                last = 0
                for i,c in enumerate(arg_temp):
                    if c in 'pw':
                        res.append(arg_temp[last:i+1])
                        last = i+1

                res = match_group(map(lambda pattern: type_group(group(pattern)), res))
                compose = list(res)
                break

    process_type()
    process_case()
    process_slicing()
    process_step()
    process_compose()

    #debug((sha_type, string, case, slicing, step, compose))
    res = sha(sha_type, string, case, slicing, step, compose)
    print(res)
    return res


def sha(type:str, string:str, case_function: Callable[[Callable], str]=str.lower, slicing:Tuple[int]=None, step:int=None, compose:List[tuple]=None) -> str:
    from hashlib import sha1, sha256, sha512

    alg = {'1': sha1, '256': sha256, '512': sha512}[type]()
    alg.update(string.encode())
    hashcode = alg.hexdigest()

    if slicing:
        start = slicing[0] if slicing[0] else 0
        stop = slicing[1] if slicing[1] else len(hashcode)
        hashcode = hashcode[start:stop]
    if compose:
        case_function = None
        temp = ''
        for group in compose:
            temp += group.case_function(hashcode[group.start:group.stop])
        hashcode = temp
    if step is not None:
        #debug(step)
        temp = ''
        assert isinstance(step, int)
        for i, c in enumerate(hashcode):
            if i and not (i % step):
                temp += ' '
            temp += c
        hashcode = temp
    if case_function:
        hashcode = case_function(hashcode)
    return hashcode


def UnknownFlagError(flag:str) -> None:
    raise F01(flag + usage(1))

def main(argv: List[str]) -> None:
    try:
        with Switch(argv[1]) as s:
            s.exit_case('--edit', edit)
            #other_cases
            #s.default(UnknownFlagError, argv[1])
            s.default(process_args, argv[1:])
    except IndexError:
        raise F00(usage(1))

if __name__ == '__main__':
    main(sys.argv)
