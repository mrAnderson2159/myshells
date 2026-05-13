import numpy as np
from random import randint
from functools import reduce
from operator import add
from os import system
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--edit":
    os.system(f"atom {__file__}")
    sys.exit(0)


matrix = np.array(
    [
        [2,8,6,8,7,4,5,6,7,8,3,8,7,6,7,7,8],
        [76,70,70,106,88,98,46,58,92,34,50,34,106,74,112,94,94],
        [27,33,39,-3,15,9,57,33,15,57,51,63,3,21,-3,15,9]
    ], dtype='int8')

redux = np.zeros(17, dtype='int8')

for i in range(3):
    redux += matrix[i]

system(f"node ~/myshells/SHA1.js {''.join(map(lambda c : chr(c), redux))} up")
