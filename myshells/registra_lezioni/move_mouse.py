#!/usr/bin/env python3

from pynput.mouse import *
from sys import argv
from time import sleep

posx, posy = map(lambda x: int(x), argv[1:])
mouse = Controller()
mouse.position = (posx + 5, posy)
sleep(.5)
mouse.move(0,50)
sleep(.5)
mouse.press(Button.left)
sleep(.1)
mouse.release(Button.left)
