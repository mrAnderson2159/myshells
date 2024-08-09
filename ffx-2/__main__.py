from src.experimento import *
import os, sys

e_missing_flag = "missing flag"

if len(sys.argv) < 2:
     raise Exception(e_missing_flag)

flag = sys.argv[1]

if flag == "--edit":
    os.system(f"atom {__file__}")
    sys.exit(0)

if flag in ('-e', '--experimento'):
    command = sys.argv[2]
    assert command in ('-a', '--add', '-d', '--del', '--delete', '-s', '--show')
    experimento = Experimento(os.path.join(sys.argv[0], 'db/experimento.json'))

    try:
        if command in ('-a', '--add'):
            _str = sys.argv[3]
            experimento.add(_str).dbwrite()
        elif command in ('-d', '--del', '--delete'):
            _str = sys.argv[3]
            experimento.delete(_str).dbwrite()
    except ArithmeticError as e:
        print(e)
    except Exception as e:
        raise e
    finally:
        experimento.p()
