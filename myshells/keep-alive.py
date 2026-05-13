from sys import argv
from pynput.mouse import Controller
from time import sleep

time = int(argv[1]) if len(argv) > 1 else 60

mouse = Controller()

while True:
    mouse.move(5,0)
    sleep(time)
    mouse.move(-5,0)
    sleep(time)
