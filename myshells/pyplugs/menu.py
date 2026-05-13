"""
Declares the Menu class which allows to instantiate a menu object which can whether return the value
the user selected or perform actions as consequence of the input.
"""

__all__ = ["Menu", "MenuInterrupt"]

__author__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

import os
from typing import *
from colors import *
from stdin import Stdin


class MenuInterrupt(Exception):
    """Raised when user types exit char"""


class Menu:
    def __init__(self,
                 name: str,
                 *,
                 intro_message: str = "Effettua una scelta",
                 exit_message: str = 'Esci',
                 return_value: bool = False,
                 auto_clean: bool = True,
                 print_name: bool = True,
                 pre_text: str = '',
                 stdin: Optional[Stdin] = None,
                 raise_ex_on_exit: bool = True
                 ) -> None:
        """This class instantiate a menu object which can whether return the value
        the user selected or perform actions as consequence of the input.

        If the user picks up an incorrect choice, an error message will be print to the screen,
        then the menu will just pop up again.

        Every menu is provided with an extra item which allows the user to leave the menu.

        It can also rely an the :class:`Stdin` queue to memorize multiple inputs.

        :param name: the name of the menu
        :param intro_message: a message to print before the panel of menu items
        :param exit_message: the name of the exit menu item
        :param return_value: a boolean used to tell the menu if the value of the item chose by the user
            is required or not. If this value is False, as it is by default, every menu item
            must be associated with a function which will be called once the user makes a choice,
            otherwise the value associated with the item will be returned
        :param auto_clean: a boolean used to tell the menu whether to clean the screen before showing or not
        :param print_name: a boolean used to tell the menu whether to show its name or not
        :param pre_text: some text to print before the intro_message
        :param raise_ex_on_exit: if is False, when the user exit the menu the value None is returned
        :param stdin: an instance of Stdin queue. If passed the menu will use the queue instead of standard
            input
        """
        self.name = name
        self.__items = []
        self.__exit_message = exit_message
        self.__intro_message = intro_message
        self.__return_value = return_value
        self.__auto_clean = auto_clean
        self.__print_name = print_name
        self.__pre_text = pre_text
        self.__stdin = stdin
        self.__raise_ex_on_exit = raise_ex_on_exit

    class MenuItem:
        def __init__(self, value: Any, text: str, action: callable, *args, **kwargs):
            """Defines a menu item.

            :param value: can be any type of value, it will be returned if the menu's return_value
                flag is set to True
            :param text: the text representing the menu item
            :param action: a function called if the menu's return_value flag is set to False
            :param args: action args
            :param kwargs: action kwargs
            """
            self.value = value
            self.text = text.capitalize().strip()
            self.action = action
            self.args = args
            self.kwargs = kwargs

        def __repr__(self):
            return str(self)

        def __str__(self):
            return f'MenuItem( {self.value} -> {self.text} )'

    def add_item(self, value: Any, text: str, action: callable = None, *args, **kwargs) -> 'Menu':
        """Adds a new menu item.

        If the menu's return_value is not required, a function must be passed to this item.

        :param value: can be any type of value, it will be returned if the menu's return_value
            flag is set to True
        :param text: the text representing the menu item
        :param action: a function called if the menu's return_value flag is set to False
        :param args: action args
        :param kwargs: action kwargs
        """
        if not self.__return_value and action is None:
            raise TypeError("add_item() requires an action function when return_value it's False")
        self.__items.append(self.MenuItem(value, text, action, *args, **kwargs))
        return self

    def remove_item(self, value: Union[str, int]) -> 'Menu':
        """Deletes an item from the menu.

        :param value: the value of the item
        """
        delis = (i for i, option in enumerate(self.__items) if option.value == value)
        for deli in delis:
            del self.__items[deli]
        return self

    def start(self) -> Any:
        """Shows the menu to the user.

        :return: if the menu's return_value flag is set to True, this will return the value of the item
            selected by the user, otherwise this will return nothing and the function associated with
            the item will be called
        :raises MenuInterrupt: when users types exit char
        """
        user_choice = 0
        while user_choice != len(self.__items) + 1:
            if self.__auto_clean:
                os.system('clear')
            if self.__print_name:
                cyan(self.name + '\n')
            menu = self.__pre_text + '\n' if self.__pre_text else ''
            menu += f'{self.__intro_message}:\n'
            for i, choice in enumerate(self.__items):
                menu += f'\t{i + 1}. {choice.text}\n'
            menu += f'\t{len(self.__items) + 1}. {self.__exit_message}'
            user_choice = self.__stdin(int, menu) if self.__stdin is not None else input(menu + '\n> ')
            try:
                user_choice = int(user_choice)
                if user_choice < 1 or user_choice > len(self.__items) + 1:
                    raise ValueError
            except ValueError:
                continue

            if user_choice != len(self.__items) + 1:
                item = self.__items[user_choice - 1]
                if self.__return_value:
                    return item.value
                else:
                    item.action(*item.args, **item.kwargs)
            else:
                if self.__raise_ex_on_exit:
                    raise MenuInterrupt
                else:
                    return None

    def __call__(self) -> Any:
        return self.start()

    @property
    def cases(self):
        return '\n'.join(map(str, self.__items))

    @property
    def items(self):
        return self.__items

    @property
    def auto_clean(self):
        return self.__auto_clean

    @property
    def print_name(self):
        return self.__print_name

    @property
    def pre_text(self):
        return self.__pre_text

    @property
    def intro_message(self):
        return self.__intro_message

    @property
    def stdin(self):
        return self.__stdin

    @property
    def exit_message(self):
        return self.__exit_message

