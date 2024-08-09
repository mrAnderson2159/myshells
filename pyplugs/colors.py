"""
Contains the definitions of functions used to text_color a portion of text or to
directly print it colored.

Available colors are red, green, yellow, blue, magenta, cyan, white.

The functions used to print colored text are named like the text_color.

The functions used to return colored text start with a c_.

The functions used to return or print bold colored text
start with a b_ if they print, with with cb_ if they return.

There's also a chance of passing some additional keyword arguments to the c_ function
as required by the colored function in the module termcolor. Available arguments are
dark, underline, blink, reverse, concealed.

Example:
    blue("Hello World")     will print a blue string;

    c_yellow("Hello World") will return a yellow text_color string;

    b_red("Hello", "World") will print a bold red string;

    cb_green("Hello World") will return a bold green strings;

    cb_red("Hello World", attrs=['underline']) will return a bold underline red string.

"""

__all__ = ['b_blue', 'b_cyan', 'b_green', 'b_magenta', 'b_red', 'b_white', 'b_yellow',
           'blue', 'c_blue', 'c_cyan', 'c_green', 'c_magenta', 'c_red', 'c_white',
           'c_yellow', 'cb_blue', 'cb_cyan', 'cb_green', 'cb_magenta', 'cb_red',
           'cb_white', 'cb_yellow', 'colored', 'cyan', 'green', 'magenta',
           'red', 'white', 'yellow'
           ]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

from termcolor import colored


def text_color(attrs=None):
    if attrs is None:
        attrs = {"attrs":[]}

    def inner(func):
        def wrapper(*args, **kwargs):
            if not len(args):
                return ""
            color, args, kwargs = func(*args, **kwargs)
            attrs.update(kwargs)
            args = map(lambda a: colored(a, color, attrs=attrs['attrs']), args)
            return ' '.join(args)

        wrapper.__doc__ = func.__doc__
        return wrapper

    return inner


def printer(attrs=None):
    if attrs is None:
        attrs = []

    def inner(func):
        def wrapper(*args, **kwargs):
            color, args, kwargs = func(*args, **kwargs)
            args = list(map(lambda a: colored(a, color, attrs=attrs), args))
            print(*args, **kwargs)

        wrapper.__doc__ = func.__doc__
        return wrapper

    return inner


@printer()
def red(*args, **kwargs):
    """Prints arguments colored in red.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'red', args, kwargs


@printer()
def green(*args, **kwargs):
    """Prints arguments colored in green.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'green', args, kwargs


@printer()
def yellow(*args, **kwargs):
    """Prints arguments colored in yellow.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'yellow', args, kwargs


@printer()
def blue(*args, **kwargs):
    """Prints arguments colored in blue.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'blue', args, kwargs


@printer()
def magenta(*args, **kwargs):
    """Prints arguments colored in magenta.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'magenta', args, kwargs


@printer()
def cyan(*args, **kwargs):
    """Prints arguments colored in cyan.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'cyan', args, kwargs


@printer()
def white(*args, **kwargs):
    """Prints arguments colored in white.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'white', args, kwargs


@printer(["bold"])
def b_red(*args, **kwargs):
    """Prints arguments colored in bold red.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'red', args, kwargs


@printer(["bold"])
def b_green(*args, **kwargs):
    """Prints arguments colored in bold green.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'green', args, kwargs


@printer(["bold"])
def b_yellow(*args, **kwargs):
    """Prints arguments colored in bold yellow.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'yellow', args, kwargs


@printer(["bold"])
def b_blue(*args, **kwargs):
    """Prints arguments colored in bold blue.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'blue', args, kwargs


@printer(["bold"])
def b_magenta(*args, **kwargs):
    """Prints arguments colored in bold magenta.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'magenta', args, kwargs


@printer(["bold"])
def b_cyan(*args, **kwargs):
    """Prints arguments colored in bold cyan.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'cyan', args, kwargs


@printer(["bold"])
def b_white(*args, **kwargs):
    """Prints arguments colored in bold white.

    :param args: arguments to print
    :param kwargs: for the built-in print function
    """
    return 'white', args, kwargs


@text_color()
def c_red(*args, **kwargs):
    """Return arguments colored in red.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'red', args, kwargs


@text_color()
def c_green(*args, **kwargs):
    """Return arguments colored in green.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'green', args, kwargs


@text_color()
def c_yellow(*args, **kwargs):
    """Return arguments colored in yellow.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'yellow', args, kwargs


@text_color()
def c_blue(*args, **kwargs):
    """Return arguments colored in blue.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'blue', args, kwargs


@text_color()
def c_magenta(*args, **kwargs):
    """Return arguments colored in magenta.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'magenta', args, kwargs


@text_color()
def c_cyan(*args, **kwargs):
    """Return arguments colored in cyan.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'cyan', args, kwargs


@text_color()
def c_white(*args, **kwargs):
    """Return arguments colored in white.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'white', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_red(*args, **kwargs):
    """Return arguments colored in bold red.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'red', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_green(*args, **kwargs):
    """Return arguments colored in bold green.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'green', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_yellow(*args, **kwargs):
    """Return arguments colored in bold yellow.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'yellow', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_blue(*args, **kwargs):
    """Return arguments colored in bold blue.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'blue', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_magenta(*args, **kwargs):
    """Return arguments colored in bold magenta.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'magenta', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_cyan(*args, **kwargs):
    """Return arguments colored in bold cyan.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'cyan', args, kwargs


@text_color({"attrs": ["bold"]})
def cb_white(*args, **kwargs):
    """Return arguments colored in bold white.

    :param args: arguments to text_color
    :param kwargs: attrs for the colored function
    """
    return 'white', args, kwargs
