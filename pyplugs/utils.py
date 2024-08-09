import os
import re
import sys
import time
from datetime import datetime, timedelta
from datetime import time as dtime
from functools import reduce
from inspect import getframeinfo, stack
from operator import add
from pathlib import Path
from statistics import mean
from typing import *


def get_parent_dir(file: str, with_slash: bool = True) -> str:
    """Returns the path to the parent dir of a file

    :param file: path to the file
    :param with_slash: (optional) to add the slash character at the end of the path (default = False)
    :return: the path to file's parent dir
    """
    return str(Path(file).parent.resolve()) + ('/' if with_slash else '')


def capitalize(string: str, all_words: bool = False) -> str:
    """Return a sentence where the first word is made uppercase, without changing
    the case of the rest of the sentence, opposite to str.capitalize().
    If the flag all_worlds is set to true then every world of the sentence
    will be capitalized.

    :param string: the sentence to be capitalized
    :param all_words: [Optional] when set to true, every world of a sentence will be
    capitalized
    :return: the capitalized sentence
    """
    if all_words:
        split_str = string.split(' ')
        cap_str = [s[0].upper() + s[1:] for s in split_str]
        return ' '.join(cap_str)
    else:
        return string[0].upper() + string[1:]


def add_zero(number: Any, precision: int) -> str:
    return str(number).zfill(precision)


def indent_lines(text: str, indentation: int) -> str:
    return '\n'.join(map(lambda line: '\t' * indentation + line, text.split('\n')))


def freq_chars(string: str) -> dict:
    freq = dict()
    for char in string:
        if char not in freq:
            freq[char] = 1
        else:
            freq[char] += 1
    return freq


def max_and_diff_ratio(element1: Union[str, int, float], element2: Union[str, int, float]) -> float:
    e1 = f"arguments must be instance of str or number, not {type(element1)}"
    e2 = f"arguments must have the same type, not {type(element1)}, {type(element2)}"
    assert type(element1) == type(element2), e2
    assert isinstance(element1, (str, int, float)), e1

    if isinstance(element1, str):
        element1 = len(element1)
        element2 = len(element2)

    m = max(element1, element2)
    d = abs(element1 - element2)
    return (m - d) / m


def extend_if_missing(main_dict: dict, extension_dict: dict) -> dict:
    e = f"arguments must be instance of dict, not {type(main_dict)}"
    assert type(main_dict) == type(extension_dict) and isinstance(main_dict, dict), e
    new_dict = main_dict.copy()
    for key in extension_dict:
        if key not in new_dict:
            new_dict[key] = extension_dict[key]
    return new_dict


def querty_close_keys(key1: str, key2: str, layout: str = 'darwin') -> float:
    if key1 == key2:
        return True

    e = f'arguments must be chars, i.e. strings of length 1, not "{key1}", "{key2}"'
    assert isinstance(key1, str) and isinstance(key2, str) and len(key1) == 1 and len(key2) == 1, e

    darwin_querty = [
        '\\|` 1!«» 2"“” 3£‘’ 4$$ 5%~‰ 6&‹› 7/÷⁄ 8(´\uf8ff 9)` 0=≠≈ \'?¡¿ ì^ˆ±',
        'qQ„‚ wWΩÀ eE€È rR®Ì tT™Ò yYæÆ uU¨Ù iIœŒ oOøØ pPπ∏ èé[{ +*]}',
        'aAåÅ sSß¯ dD∂˘ fFƒ˙ gG∞˚ hH∆¸ jJª˝ kKº˛ lL¬ˇ òç@Ç à°#∞ ù§¶◊',
        '<>≤≥ zZ∑ xX†‡ cC©Á vV√É bB∫Í nN˜Ó mMµÚ ,;… .:•· -_–'
    ]

    querty = {"darwin": darwin_querty}[layout]
    key1_row = key2_row = key1_col = 0

    for i, line in enumerate(querty):
        if key1 in line:
            key1_row = i
        if key2 in line:
            key2_row = i

    if abs(key1_row - key2_row) > 1:
        return 0.

    querty = [line.split(' ') for line in querty]
    keymap = [[-1, 0, 1], [-2, 2]]

    for i, key in enumerate(querty[key1_row]):
        if key1 in key:
            key1_col = i
            break

    for keymapping, retVal in zip([keymap[0], keymap[1]], [1., .5]):
        for key_index in keymapping:
            try:
                if key2 in querty[key2_row][key1_col + key_index]:
                    return retVal
            except IndexError:
                pass
    return 0.


def similar_strings(string1: str, string2: str, percent: bool = False) -> float:
    if string1 == string2:
        return 1.

    _res = list()

    len_res = max_and_diff_ratio(string1, string2)
    _res.append(len_res)

    freq_chars_1 = freq_chars(string1)
    freq_chars_2 = freq_chars(string2)
    all_freq_chars = extend_if_missing(freq_chars_1, freq_chars_2)
    freq_chars_res = 0.
    for char in all_freq_chars:
        if char in freq_chars_1 and char in freq_chars_2:
            freq_chars_res += max_and_diff_ratio(freq_chars_1[char], freq_chars_2[char])
    freq_chars_res /= len(all_freq_chars)
    _res.append(freq_chars_res)

    min_len = min(len(string1), len(string2))
    right_position_res = 0
    wrong_indexes = []
    for i, (char1, char2) in enumerate(zip(string1[:min_len], string2[:min_len])):
        if char1 == char2:
            right_position_res += 1
        else:
            wrong_indexes.append(i)

    right_position_res /= min_len

    _res.append(right_position_res)
    _res.append(right_position_res)

    close_keys_res = []
    for index in wrong_indexes:
        close_keys_res.append(querty_close_keys(string1[index], string2[index]))

    close_keys_res = 1 if not len(wrong_indexes) else mean(close_keys_res)
    _res.append(close_keys_res)

    if not (right_position_res or freq_chars_res):
        return 0.

    res = mean(_res)
    return round(res * 100, 2) if percent else res


def confirm(string: str, color: Callable = lambda s: s) -> bool:
    return input(color(capitalize(string) + '? (y/n): ')) in ('y', 'Y')


def clear():
    os.system('clear')


def clever_join(iterator: Iterable, conjunction: str, last_conjunction: str = ' e '):
    iterator = tuple(iterator)
    return conjunction.join(iterator[:-1]) + last_conjunction + iterator[-1]


def spaced(_list: List[str]) -> Iterator:
    max_len = max(map(len, _list))
    return map(lambda s: s + ' ' * (max_len - len(s) + 1), _list)


def remove_zeros(s: str):
    return re.sub(r'0(\d+)', r'\1', s)


def time_to_timedelta(time: dtime) -> timedelta:
    min, combine = datetime.min, datetime.combine
    return combine(min, time) - min


def seconds_to_time(s: Union[int, float]):
    s = int(s)
    t = timedelta(seconds=s)
    return (datetime.min + t).time()


def secondize(t: dtime):
    return time_to_timedelta(t).seconds


def summation(*args, add: callable = add):
    if len(args) == 1 and isinstance(args[0], (list, tuple, set)):
        args = args[0]
    return reduce(add, args)


def speed_test(function: callable) -> float:
    def wrapper(*args, **kwargs):
        t = time.time()
        f = function(*args, **kwargs)
        return f, time.time() - t

    return wrapper


def stdout_write(*args, **kwargs):
    """Print arguments without automatic \n

    :param args: print args
    :param kwargs: print kwargs
    """
    print(*args, **kwargs, end='')


def today():
    t = time.localtime()
    return t.tm_year, t.tm_mon, t.tm_mday


def get_folder_size(start_path='.', unit='b'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    units = ['b', 'k', 'm', 'g', 't']
    if unit not in units:
        unit = 'b'
    return total_size / 2 ** (10 * units.index(unit))


def install_if_missing(e: ModuleNotFoundError):
    filename = getframeinfo(stack()[1][0]).filename
    missing_package = re.search(r".* '([a-zA-Z0-9]+)'", e.msg).group(1)
    os.system(f"pip3 install {missing_package}; python3 '{filename}'")


def swap(array: list, i: int, j: int) -> None:
    array[i], array[j] = array[j], array[i]


def get_instance_attrs(self: Any) -> Set[str]:
    return {attr for attr in dir(self) if not hasattr(getattr(self, attr), '__call__') and not attr.startswith('__')}


def zprecision(number: Union[float, int, str], precision: int) -> str:
    """Add precision zeros at the end of a float number

    :param number: the float number to add zeros
    :param precision: the required precision
    :return: the precise number
    """

    if not isinstance(number, (int, float, str)):
        raise ValueError("number must be float or str")
    if isinstance(number, (int, str)):
        number = float(number)

    int_part, deg_part = str(number).split('.')
    reversed_zfill_deg_part = deg_part[::-1].zfill(precision)
    return int_part + '.' + reversed_zfill_deg_part[::-1]


def loading_bar(progress: float, char: tuple = ('*', '-'), size: int = 80):
    """Prints a loading bar to the screen.

    :param progress: a float number between 0 and 100 representing the progress
    of the bar
    :param char: [Optional] a tuple of two chars where the first one is the filling
    char, the other is the remaining char
    :param size: [Optional] the size of the bar
    """
    if not 0 <= progress <= 100.0:
        raise ValueError("The progress must be between 0 and 100")

    value = round(size * progress / 100)
    stdout_write('\r[')
    for i in range(value):
        stdout_write(char[0])
    for i in range(size - value):
        stdout_write(char[1])
    if progress < 100:
        stdout_write(f'] {zprecision(round(progress, 2), 2)}%')
    else:
        print('] 100.00%')


# def form(queries: Sequence[Sequence[str, str, type]]) -> dict:
#     """Creates a form and return the result of the queries as a dictinary.
#
#     :param queries: a matrix where each row has three colons: KEY, MESSAGE, TYPE.
#     KEY is the key of the query in the returned dictionary.
#     MESSAGE is the prompt for the user.
#     TYPE is the required type for the query, the data will be converted to the required type
#
#     :return: a dictionary built with the structure: { KEY: TYPE( input(MESSAGE) ) }
#     """
#     return {key: cast(input(msg + '\n> ')) for key, msg, cast in queries}
