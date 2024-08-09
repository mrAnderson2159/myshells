from pynput.keyboard import Listener, Key
from sys import stdout
from typing import *


class Keyboard:
    def __init__(self, command_args: Dict[str, bool],
                 allowed_commands: set[str],
                 choices: tuple[str],
                 command_list: list[str]):
        self.__str = ""
        self.__command_args = command_args
        self.__allowed_commands = allowed_commands
        self.__choices = choices
        self.__command_list = command_list

    def __manage_tab(self):
        command, *args = self.__str.split(' ')
        if command in self.allowed_commands and self.__command_args[command] and len(args) > 0:
            last = args[-1]
            for choice in self.__choices:

                if choice[:len(last)] == last:
                    self.__str = ' '.join([command, *args[:-1], choice])
                    break

    def __on_press(self, key):
        if hasattr(key, "char"):
            self.__str += key.char
        elif key is Key.space:
            self.__str += ' '
        elif key is Key.backspace:
            self.__str = self.__str[:-1] + ' '
            self.__print()
            self.__str = self.__str[:-1]
        elif key is key.tab:
            self.__manage_tab()
        elif key in (key.up, key.down):
            try:
                index = self.__command_list.index(self.__str)
            except ValueError:
                index = len(self.__command_list)
            if key is key.up:
                if index > 0:
                    self.__str = self.__command_list[index - 1]
            else:
                if index < len(self.__command_list) - 1:
                    self.__str = self.__command_list[index + 1]
        elif key is Key.enter:
            return False
        elif key is Key.esc:
            self.__str = 'ABORT'
            return False

        self.__print()

    def __print(self):
        print(f'\r> {self.__str}', end='')

    def input(self, prompt: str = ''):
        if prompt:
            print(prompt)
        print('> ', end='')
        stdout.flush()
        with Listener(
                suppress=True,
                on_press=self.__on_press) as listener:
            listener.join()
        res = self.__str
        self.__command_list.append(res)
        self.__str = ""
        print()
        return res

    def update(self, *, choices: tuple[str] = None):
        if choices is not None:
            self.__choices = choices

    @property
    def command_args(self):
        return self.__command_args

    @property
    def allowed_commands(self):
        return self.__allowed_commands

    @property
    def choices(self):
        return self.__choices
 

if __name__ == '__main__':
    command_args = {
        'ls': True,
        'cd': True,
        'pwd': False
    }

    allowed_commands = {'ls', 'cd', 'pwd'}

    choices = "StataCenter", "AthenaCluster", "AdmissionLetter"
    commands = []

    r = Keyboard(command_args, allowed_commands, choices, commands).input()
    print(r)
