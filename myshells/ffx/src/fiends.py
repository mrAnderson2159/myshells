from typing import Union, Sequence, List
from src.tool_classes import Stats, Bribe, Steal_Reward, Conquests_Stats, Species_Request
from src.functions import int_guil
from src.hashable import Hashable
from src.area import Area
from src.interfaces import *


class Fiend(Hashable):
    def __init__(self, name:str, species_conquest:Union[str, None] = None, statistics: Stats = None, capturable:bool = True, is_needed:bool = True):
        super(Fiend, self).__init__(name)
        self.species_conquest: Union[Species_Conquest, None] = Species_Conquest(species_conquest) if species_conquest else None
        if self.species_conquest:
            self.species_conquest.add(self)
        self.capturable: bool = capturable
        self.is_needed: bool = is_needed
        self.times_captured: int = 0
        self.bribe: Union[Bribe, None] = None
        self.rewards: Sequence[str] = []
        self.statistics: Stats = statistics
        self.area:Area = None

    def dict(self) -> dict:
        return {
            'name': self.name,
            'species_conquest': self.species_conquest.name if self.species_conquest else None,
            'capturable': self.capturable,
            'times_captured': self.times_captured,
            'bribe': self.bribe.dict() if self.bribe else None,
            'rewards': self.rewards,
            'statistics': self.statistics.dict() if self.statistics else None,
            'area': self.area.name if self.area else None,
            'is_needed': self.is_needed
        }

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Fiend':
        values = ['name', 'species_conquest', 'statistics', 'capturable', 'is_needed']
        dict_values = [_dict[value] for value in values]
        stats = values.index('statistics')
        dict_values[stats] = Stats.from_dict(dict_values[stats]) if dict_values[stats] else None
        fiend = cls(*dict_values)
        fiend.bribe = Bribe.from_dict(_dict['bribe']) if _dict['bribe'] else None
        fiend.area = Area(_dict['area']) if _dict['area'] else None
        fiend.set_rewards(*_dict['rewards'])
        return fiend

    def set_area(self, area:'Area'):
        self.area = area

    def set_bribe(self, guil:str, reward:str) -> None:
        bribe = Bribe(int_guil(guil), reward)
        self.bribe = bribe

    def set_rewards(self, *rewards:str) -> None:
        self.rewards = rewards

    def set_stats(self, hp:str, mp:str, ap:str, guil:str, reward:str, steal:List[str],namitec:str):
        hp, mp, ap, guil = map(lambda n: int(n) if n.isdigit() else n, [hp, mp, ap, guil])
        steal = Steal_Reward(*steal)
        namitec = namitec if namitec != '-' else None
        self.statistics = Stats(hp, mp, ap, guil, [reward], steal, namitec)

    def capture(self) -> int:
        if self.times_captured < 10:
            if self.times_captured == 0:
                self.area.add_one_captured()
            elif self.times_captured == 2:
                self.area.add_three_captured(self.species_conquest)
            elif self.times_captured == 3:
                self.area.add_four_captured(self.species_conquest)
            elif self.times_captured == 4:
                self.area.add_five_captured(self.species_conquest)
            elif self.times_captured == 9:
                self.area.add_all_captured()
            self.times_captured += 1
        return self.times_captured

    def undo_capture(self) -> int:
        if self.times_captured > 0:
            if self.times_captured == 1:
                self.area.undo_one_captured()
            elif self.times_captured == 5:
                self.area.undo_five_captured()
            elif self.times_captured == 10:
                self.area.undo_all_captured()
            self.times_captured -= 1
        return self.times_captured


class Conquest(Fiend, Conquest_Interface):
    def __init__(self, name:str, creation_reward:str = '', statistics: Stats = None):
        super(Conquest, self).__init__(name, None, statistics, False, False)
        self.creation_reward = creation_reward
        self.exists: bool = False
        self.defeated: bool = False

    def dict(self) -> dict:
        _dict = super(Conquest, self).dict()
        _dict.update({
            'creation_reward': self.creation_reward,
            'exists': self.exists,
            'defeated': self.defeated
        })
        return _dict

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Conquest':
        values = ['name', 'creation_reward', 'statistics']
        values = [_dict[value] for value in values]
        stats = values.index('statistics')
        values[stats] = Conquests_Stats.from_dict(values[stats])
        fiend = cls(*values)
        fiend.exists = _dict['exists']
        fiend.defeated = _dict['defeated']
        return fiend

class Area_Conquest(Conquest):
    def __init__(self, name:str, creation_reward:str = '', statistics: Conquests_Stats = None, area:Area = None):
        super(Area_Conquest, self).__init__(name, creation_reward, statistics)
        self.area: Area = area
        self.area.area_conquest = self

    def dict(self) -> dict:
        _dict = super(Area_Conquest, self).dict()
        _dict.update({'area':self.area.name})
        return _dict

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Area_Conquest':
        values = ['name', 'creation_reward', 'statistics', 'area']
        dict_values = [_dict[value] for value in values]
        stats, area = values.index('statistics'), values.index('area')
        dict_values[stats] = Conquests_Stats.from_dict(dict_values[stats])
        dict_values[area] = Area(dict_values[area])
        fiend = cls(*dict_values)
        fiend.exists = _dict['exists']
        fiend.defeated = _dict['defeated']
        return fiend

class Species_Conquest(Conquest):
    def __init__(self, name:str, creation_reward:str = '', statistics: Conquests_Stats = None, requests: Species_Request = None):
        super(Species_Conquest, self).__init__(name, creation_reward, statistics)
        self.requests = requests if requests else Species_Request()

    def add(self, fiend: Fiend):
        self.requests.hash_put(fiend)

    def dict(self) -> dict:
        _dict = super(Species_Conquest, self).dict()
        _dict.update({'requests':self.requests.dict()})
        return _dict

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Species_Conquest':
        values = ['name', 'creation_reward', 'statistics', 'requests']
        dict_values = [_dict[value] for value in values]
        stats, requests = values.index('statistics'), values.index('requests')
        dict_values[stats] = Conquests_Stats.from_dict(dict_values[stats])
        dict_values[requests] = Species_Request.from_dict(dict_values[requests])
        fiend = cls(*dict_values)
        fiend.exists = _dict['exists']
        fiend.defeated = _dict['defeated']
        return fiend


class Original(Conquest):
    def __init__(self, name:str, creation_reward:str = '', statistics: Conquests_Stats = None, request:str = ''):
        super(Original, self).__init__(name, creation_reward, statistics)
        self.request = request

    def dict(self) -> dict:
        _dict = super(Original, self).dict()
        _dict.update({'request':self.request})
        return _dict

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Original':
        values = ['name', 'creation_reward', 'statistics', 'request']
        dict_values = [_dict[value] for value in values]
        stats = values.index('statistics')
        dict_values[stats] = Conquests_Stats.from_dict(dict_values[stats])
        fiend = cls(*dict_values)
        fiend.exists = _dict['exists']
        fiend.defeated = _dict['defeated']
        return fiend