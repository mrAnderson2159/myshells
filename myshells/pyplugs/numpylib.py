"""
Provides useful tools for speed up common numpy operations
"""

__all__ = []

__author__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

import numpy as np


def np_map(function: callable, array: np.array, **kwargs) -> np.array:
    """Returns a copy of an array after mapping it

    :param function: the function used for mapping the array
    :param array: a numpy.array
    :return: a numpy.array copy of the mapped array
    """
    return np.array(list(map(function, array)), **kwargs)


def np_apply(function: callable, array: np.array) -> np.array:
    """Modifies an array applying a function to each element

    :param function: the function to apply to each element
    :param array: a numpy.array
    :return: the same array modified
    """
    for i in range(array.size):
        array[i] = function(array[i])
    return array
