from typing import Sequence, Union
from src.hashable import Hashable
from src.fulfill_control import Fulfill_Control

class Dict_fiend(Hashable):
    def __init__(self, name:str, data:dict):
        super().__init__(name)
        self.data = data

    def dict(self):
        pass

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Hashable':
        pass

class Area(Hashable):
    def __init__(self, name:str, size:int = 41):
        super(Area, self).__init__(name, size)
        self.area_conquest:'Area_Conquest' = None
        self.hash_table: Sequence[Union[Hashable, 'Fiend', None]]
        self.fulfill_control: Union[Fulfill_Control, None] = None
        self.all_captured = 0
        self.five_captured = 0
        self.one_captured = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Area({self.name}: {self.elements})'

    def add_one_captured(self):
        if self.one_captured < len(self):
            self.one_captured += 1
        if self.check('one_captured') == 0:
            self.fulfill_control.check_area_conquest(self.area_conquest, self.check('one_captured'))
            self.fulfill_control.check_neslug()

    def add_two_captured(self):
        if self.name == 'Monte Gagazet':
            self.fulfill_control.check_shinryu()

    def add_three_captured(self, species_conquest:'Species_Conquest'):
        self.fulfill_control.check_species_conquest(species_conquest, 3)

    def add_four_captured(self, species_conquest:'Species_Conquest'):
        self.fulfill_control.check_species_conquest(species_conquest, 4)

    def add_five_captured(self, species_conquest:'Species_Conquest'):
        if self.five_captured < len(self):
            self.five_captured += 1
            self.fulfill_control.check_species_conquest(species_conquest, 5)
        if self.check('five_captured') == 0:
            self.fulfill_control.check_ultima_buster()

    def add_all_captured(self):
        if self.all_captured < len(self):
            self.all_captured += 1
        if self.check('all_captured') == 0:
            self.fulfill_control.check_nemesis()

    def undo_one_captured(self):
        if self.one_captured > 0:
            self.one_captured -= 1

    def undo_three_captured(self):
        if self.three_captured > 0:
            self.three_captured -= 1

    def undo_four_captured(self):
        if self.four_captured > 0:
            self.four_captured -= 1

    def undo_five_captured(self):
        if self.five_captured > 0:
            self.five_captured -= 1

    def undo_all_captured(self):
        if self.all_captured > 0:
            self.all_captured -= 1
            
    def check(self, capture:str) -> int:
        choices = [attr for attr in dir(self) if not attr.startswith(('add', 'undo')) and attr.endswith('captured')]
        assert capture in choices
        return getattr(self, capture) - len(self)


    def dict(self) -> dict:
        return {
            'name': self.name,
            'size': self.N,
            'all_captured': self.all_captured,
            'five_captured': self.five_captured,
            'one_captured': self.one_captured,
            'fiends': {fiend.name: fiend.dict() for fiend in self.elements}
        }

    @classmethod
    def from_dict(cls, _dict:dict) -> 'Area':
        area = cls(_dict["name"], _dict['size'])
        values = 'all_captured','five_captured','one_captured'
        for value in values:
            setattr(area, value, _dict[value])
        for fiend, value in _dict['fiends'].items():
            area.hash_put(Dict_fiend(fiend, value))
        return area

# if __name__ == '__main__':
#     pass