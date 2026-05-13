import sys, os, re

argv = sys.argv

parameter_exception = lambda argv: Exception(f"\x1b[31mThree parameters attended (value, in/of, total) but {len(argv)-1} recevied")
preposition_exception = lambda preposition: Exception(f"\x1b[31mpreposition must be 'in' or 'of', '{preposition}' recieved")
value_exception = lambda: Exception(f"\x1b[31mvalue and total must be integers")

if len(argv) > 1 and argv[1] == '--edit':
    os.system(f"atom {argv[0]}")
    exit(0)

if len(argv[1:]) != 3:
    raise parameter_exception(argv)

try:
    value, preposition, total = argv[1:4]
    value = float(value[:-1] if re.search(r'%',value) else value)
    total = float(total)
    os.system('clear||cls')
    print(f">>> percent {' '.join(argv[1:])}\n")
    if preposition == 'in':
        print("%.2f is the %.2f%% of %.2f\n" % (value, (value * 100) / total, total))
    elif preposition == 'of':
        if re.search(r'\.0$', str(value)):
            print("%.0f%% of %.2f is %.2f\n" % (value, total, (value * total) / 100))
        else:
            print("%.2f%% of %.2f is %.2f\n" % (value, total, (value * total) / 100))
    else:
        raise preposition_exception(preposition)
except ValueError:
    raise value_exception()
