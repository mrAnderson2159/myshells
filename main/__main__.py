from src.functions.switches import *
from src.functions.errors import *
from src.functions.tools import check_and_return_args
import sys
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from switch import Switch

def main(argv: list) -> None:
    if len(argv) == 1:
        raiseMissingFlag() # src.functions.errors.raiseMissingFlag() 
    flag = argv[1]
    with Switch(flag) as s:
        s.exit_case('--edit', edit) # src.functions.switches.edit()
        s.exit_case('-i', info) # src.functions.switches.info()
        libs, *filename = check_and_return_args(argv) # src.functions.tools.check_and_return_args()
        s.case('-c', c, libs, filename) # src.functions.switches.c()
        s.case('-cpp', cpp, libs, filename) # src.functions.switches.cpp()
        s.default(raiseFlagError) # src.functions.errors.raiseFlagError()

if __name__ == '__main__':
    main(sys.argv)
