import colors
from pyerrors import *

class Verbose:
    def __init__(self, flag:bool, /, text_color:str=None, prefix:str=None):
        self.flag = flag
        self.color = color
        self.prefix = prefix

    def verbose(self, string:str, /, text_color:str=None, **kwargs) -> None:
        if self.flag:
            if color is None:
                color = self.color
            if color is not None:
                if not color in dir(colors):
                    no_colors = ('colored','new_color','print_color')
                    real_colors = ', '.join([c for c in dir(colors) if not c[:2] in ('__','c_') and c not in (no_colors)])
                    e = f"\"{color}\" is not an existing text_color function, please "
                    e += f"chose one between: {real_colors}."
                    raise I00(e)
                print_function = getattr(colors, color)
            else:
                print_function = print

            print_function((self.prefix if self.prefix else '') + string, **kwargs)
