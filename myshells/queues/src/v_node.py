"""
Defines the :class:`VNode` class inherited from :class:`Node`. VNode is used for
instantiate double linked nodes used to implement an AVL tree.
"""

import os
import sys
from functools import reduce
from operator import add
from typing import *
from binarytree import Node

from src.exceptions import NotConnectedVNodesError
from src.globals import STDIN

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from utils import get_instance_attrs
from debug import *


class VNode(Node):
    unexchangeables = {'val', 'parent', 'left', 'right'}

    def __init__(self,
                 id_val: int,
                 data: str,
                 parent: Optional['VNode'] = None,
                 left: Optional['VNode'] = None,
                 right: Optional['VNode'] = None,
                 lt_phrase: Optional[str] = None,
                 gt_phrase: Optional[str] = None
                 ) -> None:
        """This class is used for instantiate double linked nodes used to implement
        an AVL tree.


        :param id_val: a value identifier for the node, this will be "value" in :class:`Node`
        instantiation
        :param data: node's data
        :param parent: a pointer to the parent node
        :param left: a pointer to the left child node
        :param right: a pointer to the right child node
        :param lt_phrase: the phrase shown to execute the less than comparison
        :param gt_phrase: the phrase shown to execute the greater than comparison
        """
        super().__init__(id_val, left, right)
        self.parent = parent
        self.lt_phrase = lt_phrase
        self.gt_phrase = gt_phrase
        self.priority = float()
        self.data = str()
        self.hash = int()
        self.rename(data)

    def rename(self, data: str) -> None:
        """Sets the node data to a new string starting with a capital letter, then
        updates node's hash value

        :param data: the new data value for the node
        """
        data = data.strip()
        self.data = data[0].upper() + data[1:]
        self.hash = hash(self)

    def set_parent(self, other: "VNode") -> "VNode":
        """Sets the parent pointer to the other node

        :param other: the node which will become the parent of this node
        :return: the other node
        """
        self.parent = other
        return other

    def become_parent_of(self, other: "VNode") -> "VNode":
        """Makes the other parent point to this node

        :param other: the node whose parent will become this node
        :return: the other node
        """
        if other is not None:
            other.set_parent(self)
        return other

    def set_left(self, other: "VNode") -> "VNode":
        """Sets the left pointer to the other node, then sets this to the other's parent

        :param other: the node which will become this node's left child
        :return: the other node
        """
        self.left = other
        return self.become_parent_of(other)

    def set_right(self, other: "VNode") -> "VNode":
        """Sets the right pointer to the other node, then sets this to the other's parent

        :param other: the node which will become this node's right child
        :return: the other node
        """
        self.right = other
        return self.become_parent_of(other)

    def set_priority(self, priority: float) -> None:
        """Sets the priority of the object, i.e. a float number indicating if the
        node comes first or after another in the same tree

        :param priority: the priority value
        :type priority:
        """
        self.priority = priority

    def detach(self, other: "VNode") -> "VNode":
        """Separates a parent and a child, thus it sets their pointers to None

        :param other: the parent or child of this node
        :type other:
        :return: the other node
        :rtype:
        """
        if other is not None:
            if other == self.parent:
                if self == other.left:
                    other.left = None
                else:
                    other.right = None
                self.parent = None
            elif other == self.left:
                self.left = other.parent = None
            elif other == self.right:
                self.right = other.parent = None
        return other

    def swap_with_child(self, child: "VNode") -> None:
        """Swap this node with its child in the logic way, so left child will become parent
        and this will become its right child and vice versa. This is allowed only if the child
        has no children

        :param child: one of this node children
        :type child:
        :raises NotConnectedVNodesError: if the two nodes are not connected
        :raises: NotImplementedError: if user attempts to swap with a child who has got children
        """
        if child != self.left and child != self.right:
            raise NotConnectedVNodesError("Nodes are not connected")

        if child.has_children():
            raise NotImplementedError("Swap between node and child with children is not defined")

        self_parent: "VNode" = self.parent
        child_destination: str = 'left' if self_parent.left == self else 'right'
        self_destination: str = 'right' if self.left == child else 'left'
        child_position: str = 'left' if self.left == child else 'right'

        setattr(self_parent, child_destination, child)
        child.set_parent(self_parent)
        setattr(child, self_destination, self)
        self.set_parent(child)
        setattr(self, child_position, None)

    def has_left(self) -> bool:
        """Returns if the node has got a left child"""
        return self.left is not None

    def has_right(self) -> bool:
        """Returns if the node has got a right child"""
        return self.right is not None

    def has_no_children(self) -> bool:
        """Returns if the node has got no children"""
        return self.left is None and self.right is None

    def has_children(self) -> bool:
        """Returns if the node has got at least one child"""
        return not self.has_no_children()

    def has_both_children(self) -> bool:
        """Returns if the node has got both children"""
        return self.has_children() and self.right

    def is_root(self) -> bool:
        """Returns if the node has got no parent"""
        return self.parent is None

    def probable_index(self, tree_size: int, tree_min_priority: float, tree_max_priority: float) -> float:
        """
        
        :param tree_size:
        :type tree_size:
        :param tree_min_priority:
        :type tree_min_priority:
        :param tree_max_priority:
        :type tree_max_priority:
        :return:
        :rtype:
        """
        if tree_max_priority != tree_min_priority:
            return (self.priority - tree_min_priority) * tree_size / (tree_max_priority - tree_min_priority)
        return 1.

    def exchange_with(self, other: "VNode") -> "VNode":
        if not isinstance(other, self.__class__):
            raise ValueError(f"Non posso scambiare {type(self)} con {type(other)}")
        attrs = get_instance_attrs(self) - self.unexchangeables

        for attr in attrs:
            try:
                # debug((attr, getattr(self, attr), getattr(other, attr)))
                temp = getattr(other, attr)
                setattr(other, attr, getattr(self, attr))
                # debug((attr, getattr(self, attr), getattr(other, attr)))
                setattr(self, attr, temp)
                # debug((attr, getattr(self, attr), getattr(other, attr)))
            except AttributeError:
                self.unexchangeables.add(attr)

        return self

    def get_priority(self) -> float:
        return self.priority

    def __compare(self, other: "VNode") -> bool:
        print(f'\t1. {self.data}\n\t2. {other.data}')
        while (value := STDIN(int, prefix='> ')) not in (1, 2):
            red('\nIl valore inserito non è corretto: inserire 1 o 2\n')
        value -= 1
        return not value

    def __lt__(self, other: "VNode") -> bool:
        print(self.lt_phrase)
        return self.__compare(other)

    def __gt__(self, other: "VNode") -> bool:
        print(self.gt_phrase)
        return self.__compare(other)

    def __hash__(self):
        return reduce(add, map(lambda c: ord(c), self.data))


if __name__ == '__main__':
    node = VNode(0, 'mario')
    node2 = VNode(4, 'luigi')
    node.exchange_with(node2)
    print(node)
    print(node2)
