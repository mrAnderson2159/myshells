"""
Provides classes to instantiate a queue. There's a default class called QueueNode to instantiate nodes
and a Queue class to instantiate the queue.
"""

__all__ = ["QueueNode", "Queue"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

from typing import Optional, Any, TypeVar, Generic, Type
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class QueueNode:
    """This class implements a standard node with a data parameter and a next pointer to another node

    Args:
        data: Any type of data to store
        next: Pointer to next node
    """
    data: Any
    next: Optional["QueueNode"] = None


class EnqueueError(TypeError):
    """Raised when Queue.enqueue method is called and the Queue generic type is different from QueueNode"""


class Queue(Generic[T]):
    def __init__(self):
        """This class implements a FIFO queue. It's a generic class so the type of node you want
        to use must be specified
        """
        self.__queue: Optional[T] = None
        self.__tail: Optional[T] = None

    def is_empty(self):
        """Returns whether if the queue is empty or not"""
        return self.__queue is None

    def enqueue(self, data: Any, subclass: Type[T] = QueueNode) -> T:
        """Adds a new node to the tail of the queue. If the node type of this queue is different from
        default :class:`QueueNode` class, this method must at least be overwritten as it follows:

        >>> def enqueue(self, data: 'data_type', subclass: Type['NodeType'] = 'NodeType') -> 'NodeType':
        ...    return super().enqueue(data, subclass)

        :param data: Any type of data to store
        :param subclass: the node class type
        :return: the new node
        """
        generic = self.__orig_bases__[0].__args__[0]
        if not (subclass is QueueNode or generic is subclass):
            e = f"In order to use {generic.__name__} as generic type, enqueue method must " \
                f"be redefined, type help(Queue.enqueue) for further details"
            raise EnqueueError(e)

        node = QueueNode(data)
        if self.is_empty():
            self.__queue = self.__tail = node
        else:
            self.__tail.next = node
            self.__tail = self.__tail.next
        return self.__tail

    def dequeue(self) -> Any:
        """Dequeues the last element from the queue

        :return: the last element's data
        """
        if self.is_empty():
            return None

        data = self.__queue.data
        self.__queue = self.__queue.next
        return data
