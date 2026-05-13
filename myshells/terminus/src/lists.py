from typing import *
from src.game_item import GameItem


class GameItemList:
    def __init__(self, *elements: Type[GameItem]):
        self.elements: list[Type[GameItem]] = list(elements)

    def __str__(self):
        return str(self.elements)

    def __repr__(self):
        return str(self)

    def __getitem__(self, item: Union[str, int]) -> Type[GameItem]:
        if isinstance(item, str):
            index = list(map(str, self.elements)).index(item)
            return self.elements[index]
        else:
            return self.elements[item]

    def __iter__(self):
        return self.elements.__iter__()

    def __contains__(self, item: Union[str, Type[GameItem]]):
        if isinstance(item, str):
            return item in map(str, self.elements)
        else:
            return item in self.elements

    def __delitem__(self, key: Union[str, int]):
        if isinstance(key, str):
            index = list(map(str, self.elements)).index(key)
            del self.elements[index]
        else:
            del self.elements[key]

    def copy(self):
        cls = self.__class__
        print(f"debug: called copy on {cls.__name__}")
        result = cls.__new__(cls)
        for k, v in self.__dict__.items():
            setattr(result, k, v.copy() if hasattr(v, 'copy') else v)
        result.__dict__.update(self.__dict__)
        return result

    def append(self, item: Type[GameItem]):
        self.elements.append(item)


class LocationList(GameItemList):
    def __init__(self, *locations: Type['Location']):
        super(LocationList, self).__init__(*locations)


class ItemList(GameItemList):
    def __init__(self, *items: Type['Item']):
        super(ItemList, self).__init__(*items)
