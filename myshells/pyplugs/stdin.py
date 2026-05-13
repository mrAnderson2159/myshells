"""
Provides the Stdin class, which is a :class:`Queue` of :class:`Word` used to
emulate the C language input style, with some slight difference.
"""

__all__ = ["Stdin"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

from typing import Optional, Type, Sequence, Union
from pyplugs_queue import QueueNode, Queue


class Word(QueueNode):
    def __init__(self, data: str, next: Optional["Word"] = None):
        """Extends :class:`QueueNode`"""
        super().__init__(data, next)


class Stdin(Queue[Word]):
    def __init__(self):
        """This class uses a queue in order to emulate C language input style. Thus if the user enters
        more data than those required by an input, the extra data will be put inside the queue and will
        be automatically passed to the next inputs.
        """
        super().__init__()

    def enqueue(self, data: str, subclass: Type[Word] = Word) -> Word:
        return super().enqueue(data, subclass)

    def __split_res(self, split: Sequence[str]) -> str:
        """Takes the result of the split between the used input and the extra data,
        if there are extra data it enqueues them and returns the used input.

        :param split: a list made of 1 or 2 strings
        :return: the input to use
        """
        if len(split) == 2:
            res, rest = split
            self.enqueue(rest)
        else:
            res = split[0]
        return res

    def __call__(self,
                 type: type,
                 prompt: str = '',
                 sequence_len: Optional[int] = None,
                 prefix: str = '\n> ',
                 suffix: str = '\n'
                 ) -> Union[int, float, str]:
        """Asks for a typed input which can be whether numeric or a string. Before prompting a message
        to the user it checks if the queue is empty or not, if it is not empty it will dequeue the first
        value and return it as the input, else, if it is a numeric input it will split the rest and return
        the converted value, if it is a string and a sequence length of words it's specified, it will
        return the string of selected length and enqueue the rest, else it will return the whole string.


        :param type: type of the required input (str, int or float)
        :param prompt: the message to show to the user to perform the input
        :param sequence_len: in case of type:str, indicates the number of words to use
            as input (separated by a white space). The rest of words will be enqueued
        :param prefix: a string to show in the prompt before the user inserts the input
        :param suffix: a string printed after the input if this has been dequeued
        :return: the required input
        """
        if self.is_empty():
            res = input(prompt + prefix)
            new_input = True
        else:
            res = self.dequeue()
            new_input = False

        if type in (int, float):
            try:
                res = type(self.__split_res(res.split(' ', 1)))
            except ValueError:
                res = ''
        elif sequence_len is not None:
            point = 0
            if " " in res:
                for i in range(sequence_len):
                    point = res.index(' ', point) + 1

            split = res[:point - 1], res[point:]
            res = self.__split_res(split)

        if not new_input:
            print(f'{prompt}{prefix}{res}{suffix}')

        return res


if __name__ == '__main__':
    # print(help(Stdin))
    stdin = Stdin()

    nome = stdin(str, 'Come ti chiami?', 2)
    eta = stdin(int, 'Quanti anni hai?')
    altezza = stdin(float, 'Quanto sei alto?')
    professione = stdin(str, 'Che lavoro fai?')

    print(f'{nome=}\n{eta=}\n{altezza=}\n{professione=}')
