from typing import Sequence, Union, Tuple, Any, List
from src.area import Area, Dict_fiend
from src.fiends import Fiend, Species_Conquest, Area_Conquest, Original
from src.functions import int_guil
from src.hashable import Hashable
from src.tool_classes import Steal_Reward, Conquests_Stats
from src.fulfill_control import Fulfill_Control
import json
from time import time

class Zoolab(Hashable):
    def __init__(self):
        super(Zoolab, self).__init__('Zoolab', 37)
        self.hash_table: Sequence[Union[Area, None]]
        self.area_conquests: Area = Area('Campioni di zona')
        self.species_conquests: Area = Area('Campioni di specie')
        self.originals: Area = Area('Prototipi zoolab')
        self.fulfill_control: Fulfill_Control = Fulfill_Control(self, self.area_conquests, self.species_conquests, self.originals)

    def dict(self):
        return {
            'name': self.name,
            'areas': {area.name: area.dict() for area in self.elements},
            'area_conquests': self.area_conquests.dict(),
            'species_conquests': self.species_conquests.dict(),
            'originals': self.originals.dict()
        }

    @classmethod
    def from_dict(cls, _dict) -> 'Zoolab':
        zoolab = cls()
        area_conquests = Area.from_dict(_dict['area_conquests'])
        species_conquests = Area.from_dict(_dict['species_conquests'])
        originals = Area.from_dict(_dict['originals'])
        _areas = [Area.from_dict(area) for area in _dict['areas'].values()]
        areas: Sequence[Area] = [area_conquests, species_conquests, originals, *_areas]
        classes = [Area_Conquest, Species_Conquest, Original, *([Fiend]*len(_areas))]
        for i in range(len(areas)):
            area = areas[i]
            elements:Dict_fiend = area.elements
            area.reset_table()
            #print(area)
            for element in elements:
                #print(element.data)
                #print(area.hash_table)
                #print(element.data)
                fiend = classes[i].from_dict(element.data)
                species_conquest = fiend.species_conquest
                if species_conquest:
                    fiend.species_conquest = zoolab.species_conquests.hash_get(species_conquest.name)
                area.hash_put(fiend)
            if i > 2:
                zoolab.hash_put(area)
                area.fulfill_control = zoolab.fulfill_control
            else:
                area = ('area_conquests', 'species_conquests', 'originals')[i]
                setattr(zoolab, area, areas[i])
                # if i == 1:
                #     print(areas[i].hash_get('tanket').requests.elements)

        for fiend in zoolab.area_conquests.hash_table:
            if fiend is not None:
                area = zoolab.hash_get(fiend.area.name)
                fiend.area = area
                area.area_conquest = fiend
        #print(zoolab.species_conquests.hash_get('tanket').requests.elements)
        #print(zoolab['via djose']['bunyips'].species_conquest.requests.elements)
        #print()
        for area in zoolab.hash_table:
            if area is not None:
                for fiend in area.hash_table:
                    if fiend is not None:
                        fiend.area = area
                        if fiend.species_conquest:
                            species_conquest:Species_Conquest = fiend.species_conquest
                            index = species_conquest.requests.find(fiend.name)
                            species_conquest.requests.fiends[index] = fiend

        return zoolab


    def add_area(self, area:str, size:int = 0) -> Area:
        if size:
            area = Area(area, size)
        else:
            area = Area(area)
        self.hash_put(area)
        area.fulfill_control = self.fulfill_control
        return area

    def add_fiend(self, area:str, fiend:str, creates_champion:str = None) -> None:
        # noinspection PyTypeChecker
        area: Area = self.hash_get(area)
        fiend = Fiend(fiend, creates_champion)
        area.hash_put(fiend)
        fiend.set_area(area)
        try:
            conquest: Species_Conquest = self.species_conquests.hash_put(fiend.species_conquest)
            if conquest:
                conquest.add(fiend)
        except AttributeError:
            pass

    def add_area_conquest(
            self, fiend_name:str, area:str, creation_reward:str, hp:str,
            mp:str, overkill:str, steal:Tuple[str, str], reward:str, weakness:str
        ) -> None:
        hp, mp, overkill = map(int_guil, [hp, mp, overkill])
        steal = Steal_Reward(*steal)
        area = self.hash_get(area)
        stats = Conquests_Stats(hp, mp, 8000, reward, steal, overkill, weakness)
        fiend = Area_Conquest(fiend_name, creation_reward, stats, area)
        self.area_conquests.hash_put(fiend)

    def set_species_conquest(
            self, fiend_name:str, fiends_for_kind:int, creation_reward:str, hp:str,
            mp:str, overkill:str, steal:Tuple[str, str], reward:str, weakness:str
        ) -> None:
        hp, mp, overkill = map(int_guil, [hp, mp, overkill])
        steal = Steal_Reward(*steal)
        stats = Conquests_Stats(hp, mp, 8000, reward, steal, overkill, weakness)
        fiend: Species_Conquest = self.species_conquests.hash_get(fiend_name)
        fiend.requests.number = fiends_for_kind
        fiend.creation_reward = creation_reward
        fiend.statistics = stats

    def add_original(
            self, fiend_name:str, request:str, creation_reward:str, hp:str,
            mp:str, overkill:str, steal:Tuple[str, str], reward:str, weakness:str
        ) -> None:
        hp, mp, overkill = map(int_guil, [hp, mp, overkill])
        steal = Steal_Reward(*steal)
        stats = Conquests_Stats(hp, mp, 8000, reward, steal, overkill, weakness)
        fiend = Original(fiend_name, creation_reward, stats, request)
        self.originals.hash_put(fiend)


    def set_fiend_property(self, property:str, fiend_name:str, value:Any):
        areas:List[Area] = self.elements
        areas.extend([self.area_conquests, self.species_conquests, self.originals])
        fiend: Union[Fiend, None] = None
        for area in areas:
            fiend = area.hash_get(fiend_name)
            if fiend is not None:
                break
        if fiend is None:
            fiend = Fiend(fiend_name, capturable=False, is_needed=False)
            other:Area = self.hash_get('other')
            other.hash_put(fiend)
            fiend.set_area(other)
        getattr(fiend, f'set_{property}')(*value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        areas = self.elements
        areas.extend([self.area_conquests, self.species_conquests, self.originals])
        return f'Zoolab({areas})'

if __name__ == '__main__':
    with open('../database/database.json', 'r') as db:
        t = time()
        data = json.loads(db.read())
        t = time() - t
        print(f'read database {t}')
        t = time()
        zoolab = Zoolab.from_dict(data)
        t = time() - t
        print(f'build zoolab {t}')
        # fiend: Fiend = zoolab['via mihen']['elemento bianco']
        t = time() 
        for fiend in ['Elemento Bianco', 'Occhio Fluttuante', 'Rarth', 'Bikorno', 'Ipiria', 'Vivre', 'Piros', 'Mihen Phang']:
            zoolab['via mihen'][fiend].capture()
        t = time() - t
        print(f'count captured {t}')
