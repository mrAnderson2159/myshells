import sys, os

e_missing_argument = "No file provided"
e_wrong_extention = "The file must have .r extention"

if len(sys.argv) < 2:
    raise Exception(e_missing_argument)

if sys.argv[1] == "--edit":
    os.system(f"atom {__file__}")
    sys.exit(0)

f = sys.argv[1]

if f[-2:] != '.r':
    raise Exception(e_wrong_extention)

try:
    with open(f, 'r') as file:
        file.read()
    os.system(f"open {f} -a RStudio")
except FileNotFoundError:
    os.system(f"touch {f}; open {f} -a RStudio")
