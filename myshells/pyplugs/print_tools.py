"""
Provides some tools to print in fancy ways.
"""

__all__ = ["typewrite"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

import sys
from time import sleep


def typewrite(text: str, time: float = .05, end: str = '\n'):
    """Prints a string like a typewriter with a time interval between each char.

    By default at the end it prints a \\\\n char, this behavior can be modified by
    changing the "end" parameter.

    :param text: the string to print
    :param time: the time to wait between each char, 0.05s by default
    :param end: a char to print at the end of the string, endline char by default
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(time)

    print(end=end)
    # debug(time)


if __name__ == '__main__':
    typewrite("Typewriter", .3)
