"""Declares functions to menage the stdin pipe in the console"""

__all__ = ["get_pipe"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

import select
import sys


def get_pipe() -> list:
    """Returns the value piped to the program who called this function

    Example
        Program:

        >>> if __name__ == '__main__':
        >>>    print(get_pipe())

        Terminal:

        %> echo "hello world" | p piping.py

        hello world
    """
    return sys.stdin.read()[:-1] if select.select([sys.stdin, ], [], [], 0.0)[0] else []


if __name__ == '__main__':
    print(get_pipe())
