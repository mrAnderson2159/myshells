"""
Provides classes to instantiate a stack. There's a default class called StackNode to instantiate nodes
and a Stack class to instantiate the stack.
"""

__all__ = ["StackNode", "Stack"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

from typing import Optional, Any, TypeVar, Generic, Type
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class StackNode:
    """This class implements a standard node with a data parameter and a prev pointer to another node

    Args:
        data: Any type of data to store
        prev: Pointer to prev node
    """
    data: Any
    prev: Optional["StackNode"] = None


class PushError(TypeError):
    """Raised when Stack.push method is called and the Stack generic type is different from StackNode"""


class Stack(Generic[T]):
    def __init__(self):
        """This class implements a LIFO stack. It's a generic class so the type of node you want
        to use must be specified
        """
        self.__stack: Optional[T] = None

    def is_empty(self) -> bool:
        """Returns whether if the stack is empty or not"""
        return self.__stack is None

    def push(self, data: Any, subclass: Type[T] = StackNode) -> T:
        """Adds a new node to the top of the stack. If the node type of this stack is different from
        default :class:`StackNode` class, this method must at least be overwritten as it follows:

        >>> def push(self, data: 'data_type', subclass: Type['NodeType'] = 'NodeType') -> 'NodeType':
        ...    return super().push(data, subclass)

        :param data: Any type of data to store
        :param subclass: the node class type
        :return: the new node
        """
        generic = self.__orig_bases__[0].__args__[0]
        if not (subclass is StackNode or generic is subclass):
            e = f"In order to use {generic.__name__} as generic type, push method must " \
                f"be redefined, type help(Stack.push) for further details"
            raise PushError(e)

        node = subclass(data)
        if self.is_empty():
            self.__stack = node
        else:
            node.prev = self.__stack
            self.__stack = node
        return self.__stack

    def pop(self) -> Any:
        """Pops the top element from the stack

        :return: the top element's data
        """
        if self.is_empty():
            return None

        data = self.__stack.data
        self.__stack = self.__stack.prev
        return data


if __name__ == '__main__':
    stack = Stack[StackNode]()
    stack.push(7)
    stack.push('mario')
    stack.push([1,2,3])
    while not stack.is_empty():
        print(stack.pop())

    print(help(StackNode))