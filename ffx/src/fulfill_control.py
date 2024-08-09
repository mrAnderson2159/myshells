from src.interfaces import *
import os, sys
from typing import *
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from colors import *
from utils import clever_join
from src.hashable import Hashable

class Fulfill_Control:
    def __init__(self, areas: 'Area', area_conquests: 'Area', species_conquests: 'Area', originals: 'Area'):
        self.areas = areas
        self.area_conquests = area_conquests
        self.species_conquests = species_conquests
        self.originals = originals
        self.area_conquests_created = 0
        self.species_conquests_created = 0
        self.originals_created = 0

    def check_area_conquest(self, area_conquest:Union[Hashable, Conquest_Interface], fulfillment:int) -> bool:
        if fulfillment == 0:
            area_conquest.exists = True
            self.area_conquests_created += 1
            print(f'Congratulazioni hai appena creato {c_yellow(area_conquest.name)} '
                  f'avendo catturato ciascun esemplare dei mostri a {c_yellow(area_conquest.area.name)}, '
                  f'riceverai {c_cyan(area_conquest.creation_reward)} come ricompensa!')
            if self.area_conquests_created == 2:
                self.check_earth_eater()
            elif self.area_conquests_created == 6:
                self.check_catastrophe()
            elif self.area_conquests_created == 10:
                self.check_nemesis()
            return True
        return False


    def check_species_conquest(self, species_conquest: 'Species_Conquest', number: int) -> bool:
        if species_conquest.requests.number == number:
            for fiend in species_conquest.requests.elements:
                if fiend.times_captured < number:
                    return False
            species_conquest.exists = True
            self.species_conquests_created += 1
            print(f'Congratulazioni hai appena creato {c_yellow(species_conquest.name)} '
                  f'avendo catturato {number} esemplari di '
                  f'{clever_join(map(lambda f:c_yellow(f.name), species_conquest.requests.elements), ", ", " e " )}, '
                  f'riceverai {c_cyan(species_conquest.creation_reward)} come ricompensa!')
            if self.species_conquests_created == 2:
                self.check_greater_sphere()
            elif self.species_conquests_created == 6:
                self.check_thuban()
            elif self.species_conquests_created == 10:
                self.check_nemesis()
            return True
        return False

    def check_earth_eater(self) -> bool:
        if self.area_conquests_created == 2:
            fiend = self.originals.hash_get('mangiaterra')
            fiend.exists = True
            print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
                  f'avendo creato due esemplari della categoria {c_yellow("Campioni di zona")}, '
                  f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
            return True
        return False

    def check_greater_sphere(self) -> bool:
        if self.species_conquests_created == 2:
            fiend = self.originals.hash_get('titanosfera')
            fiend.exists = True
            print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
                  f'avendo creato due esemplari della categoria {c_yellow("Campioni di specie")}, '
                  f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
            return True
        return False

    def check_catastrophe(self) -> bool:
        if self.area_conquests_created == 6:
            fiend = self.originals.hash_get('catastrophe')
            fiend.exists = True
            print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
                  f'avendo creato sei esemplari della categoria {c_yellow("Campioni di zona")}, '
                  f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
            return True
        return False

    def check_thuban(self) -> bool:
        if self.species_conquests_created == 2:
            fiend = self.originals.hash_get('vlakorados')
            fiend.exists = True
            print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
                  f'avendo creato due esemplari della categoria {c_yellow("Campioni di specie")}, '
                  f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
            return True
        return False

    def check_neslug(self) -> bool:
        for area in self.areas.elements:
            if area.name == 'Other':
                continue
            elif area.check('one_captured') < 0:
                return False
        fiend = self.originals.hash_get('gasteropodos')
        fiend.exists = True
        print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
              f'avendo catturato un esemplare di ogni mostro su Spira, '
              f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
        return True

    def check_ultima_buster(self):
        for area in self.areas.elements:
            if area.name == 'Other':
                continue
            elif area.check('five_captured') < 0:
                return False
        fiend = self.originals.hash_get('ultima x')
        fiend.exists = True
        print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
              f'avendo catturato cinque esemplari di ogni mostro su Spira, '
              f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
        return True

    def check_shinryu(self):
        gagazet = self.areas.hash_get('monte gagazet')
        splasher = gagazet.hash_get('splasher')
        aquelous = gagazet.hash_get('aquelous')
        echenesis = gagazet.hash_get('echenesis')
        required = (splasher, aquelous, echenesis)
        if all(map(lambda n: n > 1, required)):
            fiend = self.originals.hash_get('shinryu')
            fiend.exists = True
            print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
                  f'avendo catturato due esemplari {clever_join(required, ", ", " e ")} al monte gagazet, '
                  f'riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
            return True

    def check_nemesis(self):
        for area in self.areas.elements:
            if area.name == 'Other':
                continue
            elif area.check('all_captured') < 0:
                return False
        for area in (self.area_conquests.elements, self.species_conquests.elements, self.originals.elements):
            for fiend in area:
                if fiend.name == 'Il Supremo':
                    continue
                if not fiend.was_defeated:
                    return False

        fiend = self.originals.hash_get('il supremo')
        fiend.exists = True
        print(f'Congratulazioni hai appena creato {c_yellow(fiend.name)} '
              f'avendo catturato dieci esemplari di ogni mostro su Spira, sconfitto tutti i campioni di zona, i campioni di specie e i prototipi zoolab! '
              f'Riceverai {c_cyan(fiend.creation_reward)} come ricompensa!')
        return True