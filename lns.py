from os import system, path, getcwd
import sys, re

e_missing_arguments = "this program needs the path to the origin and the path to the link to work"

if len(sys.argv) == 2 and sys.argv[1] == "--edit":
    os.system(f"atom {__file__}")
    sys.exit(0)
elif len(sys.argv) < 3:
     raise Exception(e_missing_arguments)

origin, link = sys.argv[1:]
current_path = getcwd() + '/'

regex = re.compile('^'+current_path)
if not (re.match(regex, origin) or re.match(r'^\/', origin)):
    origin = current_path + origin

print(f"{origin} -> {link}")

system(f"ln -s {origin} {link}")
