import subprocess, os, sys

e1 = "killer needs the process name to work, pass an argument"

if len(sys.argv) == 1:
    raise Exception(e1)
elif len(sys.argv) > 1 and sys.argv[1] == "--edit":
    os.system(f"atom {__file__}")
    sys.exit(0)
else:
    res = subprocess.run(['pidof',sys.argv[1]],  stdout=subprocess.PIPE)
    processes = res.stdout.decode().split()
    for p in processes:
        os.system(f"kill {p}")
