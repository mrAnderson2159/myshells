from functools import reduce
from operator import add
import sys, os

length = len(sys.argv) - 1

if length != 1:
    raise Exception(f"portify takes exactly 1 argument (<name>), {length} recieved")

name = sys.argv[1]

if name == '--edit':
    os.system(f"atom {sys.argv[0]}")
    sys.exit(0)

if len(name) != 4:
    raise Exception(f"<name> must be 4 character long, {name} is " + ("too long" if len(name) > 4 else "not long enaugh"))

in_ord = [str(ord(c)) for c in name]
matrified = [[int(n) for n in s] for s in in_ord]
reduced = [str(reduce(add, arr) % 10)for arr in matrified]
port = ''.join(reduced)
print(port)
