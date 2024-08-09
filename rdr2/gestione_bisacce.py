from typing import List, Optional
from json import loads


class Bisaccia:
    def __init__(self, name: str, requests: List[str]):
        """Rappresenta una bisaccia di Arthur che Pearson può migliorare

        :param name: il nome della bisaccia
        :param requests: rappresenta l'elenco di pelli richieste per migliorare l'oggetto
        """
        self.name = name
        self.requests = requests

    def contains(self, request: str) -> Optional[str]:
        """Restituisce il nome di questa bisaccia se contiene l'oggetto richiesto

        :param request: l'oggetto che deve contenere questa bisaccia
        :type request:
        :return: il nome di questa bisaccia
        :rtype:
        """
        if request in self.requests:
            return self.name
        return None

    def __str__(self):
        return f"Bisaccia({self.name}: {', '.join(self.requests)})"

    def __repr__(self):
        return str(self)


class Inventario:
    def __init__(self, bisacce_json_path: str):
        """Class documentation"""
        with open(bisacce_json_path, 'r') as bisacce:
            inventario = loads(bisacce.read())
            self.inventory = []
            for bisaccia in inventario:
                self.inventory.append(Bisaccia(bisaccia, inventario[bisaccia]))

    def count(self) -> dict:
        freq = {}
        for bisaccia in self.inventory:
            for request in bisaccia.requests:
                if request in freq:
                    freq[request] += 1
                else:
                    freq[request] = 1
        return freq

    def contains(self, request: str) -> list:
        return [bisaccia.name for bisaccia in self.inventory if bisaccia.contains(request)]

    def find(self, bisaccia: str) -> Optional[int]:
        for i, b in enumerate(self.inventory):
            if b.name == bisaccia:
                return i
        return None

    def __getitem__(self, key: str) -> Bisaccia:
        index = self.find(key)
        return self.inventory[index]

    def __setitem__(self, key, value):
        if isinstance(value, Bisaccia):
            self.inventory.append(value)
        else:
            if not (isinstance(value, (tuple, list))
                    or len(value) == 2
                    or isinstance(value[0], str)
                    or isinstance(value[1], (tuple, list))):
                raise ValueError("Value must be a Tuple[str, Tuple[str]] containing the name "
                                 f"and the required skins, {value} is not valid")
            self.inventory.append(Bisaccia(*value))

    def __delitem__(self, bisaccia: str):
        index = self.find(bisaccia)
        del self.inventory[index]

    def __str__(self):
        return str(self.inventory)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    inventario = Inventario('pelli per bisacce.json')

    del inventario['provviste']
    del inventario['oggetti preziosi']
    del inventario['ingredienti']

    count = inventario.count()
    print(count, '\n')
    print(inventario)
