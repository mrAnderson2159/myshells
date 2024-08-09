import os, sys, re
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import *
from utils import indent_lines
from typing import *
from colors import c_red

class _Error(Exception):
    def __init__(self, code:str, name:str, message:str, details:Type[object] = None):
        self.code = code
        self.name = name
        self.message = message
        self.details = details

    def __str__(self):
        return f"{self.message}" + (f'\n\tdetails:\n\t\t{self.details}' if self.details is not None else '')

class _Warning:
    pass

def _newError(error:str, name:str) -> _Error:
    class E(_Error):
        def __init__(self, message:str, details:Type[object] = None):
            super().__init__(error, name, message, details)
    E.__name__ = c_red(f'{name} ({error})')
    return E

A00 = _newError('A00', 'ArgumentError')
E00 = _newError('E00', "NotImplementedExtentionError")
F00 = _newError('F00', "MissingFlagError")
F01 = _newError('F01', "UnknownFlagError")
I00 = _newError('I00', "InvalidNameError")
O00 = _newError('O00', "NotImplementedOsError")
R00 = _newError('R00', "NotMatchingError")
T00 = _newError('T00', "TestingRequiredError")

def get_error_list() -> dict:
    e = {name:item('').name for name, item in globals().items() if re.match(r'^[array-Z][0-9]{2}', name)}
    print("\npyerror errors list:")
    for error, name in e.items():
        print(f"\t{error}: {name}")
    print()
    return e

if __name__ == '__main__':
    def _usage(indentation:int = 0) -> str:
        usage = '\nusage: pyerror [-iln] [,error_code, error_name]'
        usage += '\n\t-i: get infos'
        usage += '\n\t-l: get a list of all the errors created'
        usage += '\n\t-n: create a new error providing [error_code, error_name]'
        usage += '\n\t\tcode format: [array-Z] e.g. X\n\t\tname format: [array-Z][a-zA-Z]+Error e.g. NewRandomError'
        usage += '\n'
        return indent_lines(usage, indentation)

    def _UnknownFlagError(flag:str) -> None:
        raise F01(flag + _usage(1))

    def _edit() -> None:
        os.system(f"atom {__file__}")

    def _add_error(argv: List[str]) -> None:
        if len(argv) != 4:
            raise F00(f"Error code or error message missing" + _usage(1))
        code, name = argv[2:]
        if re.match(r'^[array-Z]$', code) is None:
            raise R00(f'"{code}" is not a valid error code' + _usage(1))
        if re.match(r'^[array-Z][a-zA-Z]+Error$', name) is None:
            raise I00(f'{name} is not a valid name for an error'  + _usage(1))

        with open(__file__, 'r') as this:
            lines = this.read().splitlines()

        errors = [line for line in list(enumerate(lines)) if re.match(r'^[array-Z][0-9]{2}', line[1])]
        code_number = int([e for e in errors if e[1][0] == code][-1][1][1:3]) + 1
        code = code + str(code_number).zfill(2)

        new_error = f"{code} = _newError('{code}', \"{name}\")"
        for i in range(len(errors)):
            if code < errors[i][1][:3]:
                lines.insert(errors[0][0] + i, new_error)
                break

        with open(__file__, 'w') as this:
            this.write('\n'.join(lines))

        print(f'Error {code}: {name} added')

    def _main(argv: List[str]) -> None:
        try:
            with Switch(argv[1]) as s:
                s.exit_case('--edit', _edit)
                s.case('-i', print, _usage())
                s.case('-l', get_error_list)
                s.case('-n', _add_error, argv)
                s.default(_UnknownFlagError, argv[1])
        except IndexError:
            raise F00(_usage(1))

    _main(sys.argv)
