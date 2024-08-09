import os
import sys
from typing import *

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from debug import debug


class VTreeDict:
    def __init__(self, name: str, phrases: Tuple[str, str], tree: Dict[str, dict], completed=None):
        if completed is None:
            completed = []
        self.name = name
        self.phrases = phrases
        self.tree = tree
        self.completed = completed

    def dict(self):
        return {
            'name': self.name,
            'phrases': self.phrases,
            'tree': self.tree,
            'completed': self.completed
        }

    def __repr__(self):
        return self.dict()

    def __str__(self):
        return str(self.dict())

    @staticmethod
    def dictize(dict_tree: dict) -> "VTreeDict":
        dk = set(dict_tree.keys())
        sk = {'name', 'phrases', 'tree', 'completed'}
        if dk != sk:
            debug(dict_tree)
            raise ValueError(f"Il dizionario non presenta un formato valido, valori mancanti: {sk - dk}")
        name = dict_tree['name']
        phrases = dict_tree['phrases']
        tree = dict_tree['tree']
        completed = dict_tree['completed']
        return VTreeDict(name, phrases, tree, completed)
