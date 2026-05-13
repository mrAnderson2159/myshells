from pynput.mouse import Controller
from time import sleep
mouse = Controller()
d = 1
while True:
    mouse.move(100*d,0)
    d = -d
    sleep(30)
