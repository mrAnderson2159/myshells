from pynput.mouse import *
from time import sleep

mouse = Controller()
mouse.position = (1525, 924)
sleep(.5)
mouse.click(Button.left, 2)
