from functools import reduce
from operator import add
from typing import Any, Union, List
from abc import ABC, abstractmethod

from src.exceptions import FullTableException
from src.functions import ffx_cap, camel_split

class Hashable(ABC):
    def __init__(self, name:str, N:int = 0):
        '''
        Allows to implement an hash table.

        This class provide methods to encode and compress the key (name) of an object
        in order to store it inside an hash table. By default the size of the hash table
        is set to 0 because many subclasses are not interested in using it, they just need
        to hash their instances. When the size of the hash table is provided, the class will
        be allowed to use the hash table and the connected methods. It's recommended to use
        a dimension twice as big as the number of elements you want to store.

        :param name: the name or key of the object
        :type name: str
        :param N: [Optional] the size of the hash table
        :type N: Optional[int]
        '''
        self.name = ffx_cap(camel_split(name))
        self.N = N
        self.hash_table: Any = [None] * N
        self.hash_code = hash(self)
        self.occupied = 0

    def __hash__(self) -> int:
        '''Encodes the key of this object using Hashtable.encode method

        :return: encoded key
        :rtype: int
        '''
        return self.encode(self.name)

    def __getitem__(self, key:str) -> 'Hashable':
        return self.hash_get(key)

    def encode(self, key):
        '''Encodes a key by summing the ascii value of each character

        :param key: the key of an object
        :type key: str
        :return: encoded key
        :rtype: int
        '''
        return reduce(add, map(lambda c: ord(c), key))

    def compress(self, hash_key:int) -> int:
        '''Compresses an hash code to fit into the hash table of this instance.

        :param hash_key: a key hashed with the Hashable.encode method
        :type hash_key: int
        :return: compressed key
        :rtype: int
        '''
        return hash_key % self.N

    def hash_put(self, element:'Hashable') -> Union['Hashable', None]:
        '''Puts an hashable object inside hash table of this instance.

        :param element: an object instance of a subclass of Hashable
        :type element: Hashable
        :return: Nothing if the element is new inside the hash table or the already existing element
        :rtype: None | Hashable
        :raise FullTableException: if the table is already full (half full)
        '''
        # :raise ObjectAlreadyStoredException: if there is already an object with same key
        # stored inside the hash table
        if self.occupied == self.N // 2:
            raise FullTableException(self)
        i = 0
        index = self.compress(element.hash_code)
        while (current := self.hash_table[(index + i) % self.N]) is not None:
            if current.name == element.name:
                return current
            i += 1
        self.hash_table[(index + i) % self.N] = element
        self.occupied += 1
        return None

    def hash_get(self, key: str) -> Union['Hashable', None]:
        '''Return an hashable object inside the hash table searched by its key.
        If the object is not found, None is returned.

        :param key: key of the searched object
        :type key: str
        :return: the result of the search
        :rtype: Hashable | None
        '''
        i = 0
        key = ffx_cap(camel_split(key))
        index = self.compress(self.encode(key))
        while (current := self.hash_table[(index + i) % self.N]) is not None:
            if current.name == key:
                return current
            i += 1
        return None

    def find(self, key: str) -> Union[int, None]:
        i = 0
        key = ffx_cap(camel_split(key))
        index = self.compress(self.encode(key))
        while (current := self.hash_table[(index + i) % self.N]) is not None:
            if current.name == key:
                return (index + i) % self.N
            i += 1
        return None

    def reset_table(self):
        self.hash_table = [None] * self.N
        self.occupied = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}({self.name})'

    @abstractmethod
    def dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, _dict:dict) -> 'Hashable':
        pass

    @property
    def elements(self) -> List['Hashable']:
        res = []
        for element in self.hash_table:
            if element is not None:
                res.append(element)
        return res

    def __len__(self) -> int:
        i = 0
        for element in self.hash_table:
            if element is not None:
                i += 1
        return i