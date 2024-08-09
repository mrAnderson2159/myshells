from typing import Callable
from src.game_item import GameItem


class Item(GameItem):
    def __init__(self, name: str,
                 content: Callable[[], None],
                 *,
                 movable: bool = False):
        super().__init__(name)
        self.content = content
        self.movable = movable

    def less(self):
        self.content()
