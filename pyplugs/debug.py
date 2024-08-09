"""
Contains tools for debugging.

The "debug" function prints the name of the file who called it and
the line where did the call come from, then it prints the arguments.

The "Status" class allows to keep track of named variables inside functions.
"""

__all__ = ["debug", "Status"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

from inspect import currentframe, getframeinfo, stack
from typing import Sequence, Optional

from colors import cyan, yellow, c_cyan, c_yellow, c_magenta


def debug(*args, **kwargs):
    """Prints the name of the file who called it and the line where did the call come from,
    then it prints the arguments.

    :param args: the arguments to be debugged
    :param kwargs: keyword arguments for the cyan function in pyplugs.colors module
    """
    caller = getframeinfo(stack()[1][0])
    yellow(f"Debugging file {caller.filename} at line {caller.lineno}:", end='\n\t')
    cyan(*args, **kwargs)


class Status:
    def __init__(self, variables: str, show: bool = True):
        """Instantiate a callable object who prints the file and the line where it was called,
        then it prints the name and value of the variables it must track if they are already
        defined.

        An optional value named "show" allows to print or not the tracking.

        :param variables: array string containing the name of all the variables to track
        separated by a white space
        :param show: array boolean indicating whether to show the tracking or not
        """
        self.variables: Sequence[str] = variables.split(' ')
        self.show = show
        self.caller = currentframe().f_back

    def __call__(self, position: str) -> Optional[str]:
        """Returns the name and the value of the variables this object must track.
        If the show flag of this object is on, they will be printed.

        Example:
            >>> def foo(n):
            ...     status = Status('n a b c')
            ...     a = n
            ...     b = 2*n - 1
            ...     status("before loop")
            ...     for i in range(3):
            ...             c = a*b - a+b
            ...             a += b
            ...             b = c - a
            ...             status("inside loop")
            ...     status("after loop")
            ...
            >>> foo(5)
            File <stdin> at line 5:
            Function foo at before loop:

                n: 5
                a: 5
                b: 9

            File <stdin> at line 10:
            Function foo at inside loop:

                n: 5
                a: 14
                b: 35
                c: 49

            File <stdin> at line 10:
            Function foo at inside loop:

                n: 5
                a: 49
                b: 462
                c: 511

            File <stdin> at line 11:
            Function foo at after loop:

                n: 5
                a: 49
                b: 462
                c: 511

        :param position: a string indicating the point where the function was called
        :return: file name, file line, name and value of the variables
        """
        file_info = getframeinfo(stack()[1][0])
        filename = file_info.filename
        line = file_info.lineno
        caller_name = c_magenta(self.caller.f_code.co_name)
        at_point = c_yellow(position)
        caller_args = [(var, value) for var, value in list(self.caller.f_locals.items())
                       if var in self.variables]
        caller_args = '\n\t'.join(map(lambda t: f'{c_yellow(t[0])}: {str(t[1])}', caller_args))

        res = f"{c_cyan('File')} {filename} {c_cyan('at line')} {line}:\n" \
            + f"{c_cyan('Function')} {caller_name} {c_cyan('at')} {at_point}:" \
            f"\n\n\t{caller_args}\n"

        if self.show:
            print(res)

        return res


if __name__ == '__main__':
    def foo(n):
        status = Status('n a b c')
        a = n
        b = 2 * n - 1
        status("before loop")
        for i in range(2):
            c = a * b - a + b
            a += b
            b = c - a
            status("inside loop")
        status("after loop")

    foo(5)
