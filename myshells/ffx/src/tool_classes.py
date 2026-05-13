from typing import Sequence, Union
from src.hashable import Hashable
from src.area import Dict_fiend

class Bribe:
    def __init__(self, guil:int, reward:str):
        '''Represents a bribe between the player and a fiend, guil payed and objects obtained.

        :param guil: the amount of guil player has to pay to the fiend
        :type guil: int
        :param reward: the amount of objects obtained as reward
        :type reward: str
        '''
        self.guil = guil
        self.reward = reward

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}({self.guil} guil x {self.reward})'

    def dict(self) -> dict:
        return {
            'guil': self.guil,
            'reward': self.reward
        }

    @classmethod
    def from_dict(cls, _dict) -> 'Bribe':
        return cls(_dict['guil'], _dict['reward'])

class Steal_Reward:
    def __init__(self, normal:str, rare:str):
        '''Represents the objects player gets by stealing from a fiend. Normal or rare reward.

        :param normal: object obtained in most cases
        :type normal: str
        :param rare: object rarely obtained
        :type rare: str
        '''
        self.normal = normal
        self.rare = rare

    def __repr__(self):
        return str(self)

    def __str__(self):
        normal = self.normal
        rare = self.rare
        return f'{self.__class__.__name__}({normal=}, {rare=})'

    def dict(self) -> dict:
        return {
            'normal': self.normal,
            'rare': self.rare
        }

    @classmethod
    def from_dict(cls, _dict) -> 'Steal_Reward':
        return cls(_dict['normal'], _dict['rare'])


class Stats:
    def __init__(self, hp:int, mp:int, ap:int, guil:int, rewards:Sequence[str], steal: Steal_Reward, namitec:Union[str, None]):
        self.hp: int = hp
        self.mp: int = mp
        self.ap: int = ap
        self.guil: int = guil
        self.rewards: Sequence[str]  = rewards
        self.steal: Steal_Reward = steal
        self.namitec = namitec

    def dict(self) -> dict:
        return {
            'hp': self.hp,
            'mp': self.mp,
            'ap': self.ap,
            'guil': self.guil,
            'rewards': self.rewards,
            'steal': self.steal.dict(),
            'namitec': self.namitec,
        }

    @classmethod
    def from_dict(cls, _dict) -> 'Stats':
        values = ['hp', 'mp', 'ap', 'guil', 'rewards', 'steal', 'namitec']
        dict_values = [_dict[value] for value in values]
        steal = values.index('steal')
        dict_values[steal] = Steal_Reward.from_dict(dict_values[steal])
        return cls(*dict_values)

    def __repr__(self):
        return str(self)

    def __str__(self):
        hp = self.hp
        mp = self.mp
        ap = self.ap
        guil = self.guil
        rewards = self.rewards
        steal = self.steal
        namitec = self.namitec
        return f'{self.__class__.__name__}({hp=}, {mp=}, {ap=}, {guil=}, {rewards=}, {steal=}, {namitec=})'


class Conquests_Stats(Stats):
    def __init__(self, hp:int, mp:int, ap:int, rewards:Sequence[str], steal: Steal_Reward, overkill:int, weakness:str):
        super(Conquests_Stats, self).__init__(hp, mp, ap, 0, rewards, steal, None)
        self.overkill = overkill
        self.weakness = weakness

    def dict(self) -> dict:
        _dict = super().dict()
        _dict.update({
            'overkill': self.overkill,
            'weakness': self.weakness
        })
        return _dict

    @classmethod
    def from_dict(cls, _dict) -> 'Conquests_Stats':
        values = ['hp', 'mp', 'ap', 'rewards', 'steal', 'overkill', 'weakness']
        dict_values = [_dict[value] for value in values]
        steal = values.index('steal')
        dict_values[steal] = Steal_Reward.from_dict(dict_values[steal])
        return cls(*dict_values)


class Species_Request(Hashable):
    def __init__(self, number: int = 0):
        super().__init__('species request', 29)
        self.fiends = self.hash_table
        self.number = number

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Species_Request({self.number} of {self.elements})'

    def dict(self):
        return {
            'fiends': list(map(lambda f:f.name, self.elements)),
            'number': self.number
        }

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Species_Request':
        request = cls(_dict['number'])
        for fiend in _dict['fiends']:
            request.hash_put(Dict_fiend(fiend, {'name':fiend}))
        return request