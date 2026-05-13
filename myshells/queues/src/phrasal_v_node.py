"""
Defines the :class:`PhrasalVNode` class which allows to instantiate a :class:`VNode` object
with preset "lt_phrase" and "gt_phrase" attributes
"""

from src.v_node import VNode


class PhrasalVNode:
    def __init__(self, lt_phrase: str, gt_phrase: str) -> None:
        """ This is support class for :class:`VNode`, allows to instantiate a VNode
        object with preset "lt_phrase" and "gt_phrase" attributes

        :param lt_phrase: used for less than operator comparison
        :type lt_phrase: str
        :param gt_phrase: used for greater than operator comparison
        :type gt_phrase: str
        """
        self.lt_phrase = lt_phrase
        self.gt_phrase = gt_phrase

    def __call__(self, *args, **kwargs) -> VNode:
        """Returns a :class:`VNode` instance with lt_phrase and gt_phrase defined
        in this class

        :return: VNode instance
        :rtype: VNode
        """
        return VNode(*args, **kwargs, lt_phrase=self.lt_phrase, gt_phrase=self.gt_phrase)
