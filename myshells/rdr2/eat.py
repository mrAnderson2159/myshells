from playsound import playsound
from time import time, sleep
from threading import Thread, Lock
from pynput.keyboard import Listener, HotKey
from sys import path
from os.path import expanduser
from os import system

path.append(expanduser('~/myshells/pyplugs'))
from colors import yellow, cyan, c_yellow, c_cyan
# from debug import debug


class Meal:
    def __init__(self):
        """Class documentation"""
        self.waits = 7, 7, 10
        self.meals = "Fai colazione", "Pranza", "Cena"
        self.index = 2
        self.game_speed = 17

    def wait(self) -> int:
        return self.waits[self.index]

    def eat(self) -> str:
        return self.meals[self.index]

    def increase(self, lock: Lock):
        lock.acquire()
        self.index = (self.index + 1) % 3
        self.next()
        lock.release()

    def play(self):
        submarine = '/System/Library/Sounds/Submarine.aiff'
        playsound(submarine)

    def next(self):
        yellow(self.eat())
        self.play()
        cyan(f"Il prossimo pasto è tra {c_yellow(round(self.wait() * 60 / self.game_speed))} {c_cyan('minuti')}\n")


class Sleeper(Thread):
    def __init__(self, meal: Meal, lock: Lock):
        Thread.__init__(self)
        self.meal = meal
        self.time = 0
        self.lock = lock
        self.light = 1

    def reset(self):
        self.time = self.meal.wait() * 3600 / self.meal.game_speed + time()

    def run(self):
        while self.light:
            if time() < self.time:
                sleep(1)
            else:
                self.meal.increase(self.lock)
                self.reset()

    def stop(self):
        self.light = 0


class Main:
    def __init__(self, meal: Meal, sleeper: Sleeper, lock: Lock):
        self.meal = meal
        self.sleeper = sleeper
        self.lock = lock
        self.hotkey = HotKey(HotKey.parse('<cmd>+<enter>'), self.on_activate)

    def on_activate(self):
        sleep(.1)
        print('\r', end='')
        self.meal.increase(self.lock)
        self.sleeper.reset()

    def for_canonical(self, func):
        return lambda k: func(Listener.canonical(None, k))

    def start(self):
        system('clear')
        try:
            self.sleeper.start()
            with Listener(on_press=self.for_canonical(self.hotkey.press),
                          on_release=self.for_canonical(self.hotkey.release)) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.sleeper.stop()
            print('\r', end='')


if __name__ == '__main__':
    lock = Lock()
    meal = Meal()

    sleeper = Sleeper(meal, lock)
    main = Main(meal, sleeper, lock)

    main.start()
