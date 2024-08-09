from src.messages import Messages
from src.lists import LocationList, ItemList
from src.location import Location
from src.item import Item

while (gender := input("Ciao! Inserisci il tuo genere (m/f):\n> ").lower()) not in ('m','f'):
        print("Non ho capito, inserisci se sei maschio (m) o femmina (f)")

m = Messages(gender)
DEFAULT_COMMANDS = {'clear', 'cd', 'help', 'ls', 'less', 'man', 'pwd'}
EMPTY = Location("", None, LocationList(), ItemList(),  DEFAULT_COMMANDS)


PRACTICE_ROOM = Location("StanzaDellaProva",
                         m.practice_room,
                         LocationList(
                             Location("Scatola", m.box, LocationList(), ItemList(),  {''}, is_accessible=False)
                         ),
                         ItemList(
                             Item("Istruzioni", m.instructions),
                             *[Item(f'{m.dummy_name()}{i+1}', m.dummy, movable=True) for i in range(5)]
                         ),
                         DEFAULT_COMMANDS | {'mv'},
                         is_resettable=True)

LESSONS = Location("Lezioni",
                   m.lessons,
                   LocationList(),
                   ItemList(
                       Item("Professore", m.professor)
                   ),
                   DEFAULT_COMMANDS)

SPELL_CASTING_ACCADEMY = Location("AccademiaDiIncantesimi",
                                  m.spell_casting_accademy,
                                  LocationList(PRACTICE_ROOM, LESSONS),
                                  ItemList(
                                      Item(m.hurryng_student_name(), m.hurryng_student)
                                  ),
                                  DEFAULT_COMMANDS)

WESTERN_FOREST = Location("ForestaDell'Ovest",
                          m.western_forest,
                          LocationList(SPELL_CASTING_ACCADEMY),
                          ItemList(
                              Item("InsegnaDellaScuola", m.sign),
                              Item("Indicazione", m.backsign)
                          ),
                          DEFAULT_COMMANDS)

CAVE = Location("Caverna",
                None,
                LocationList(),
                ItemList(),
                DEFAULT_COMMANDS)

EASTERN_MOUNTAINS = Location("MontagneDell'Est",
                             m.eastern_mountains,
                             LocationList(CAVE),
                             ItemList(
                                 Item("UomoAnziano", m.old_man),
                                 Item("AnticoManoscritto", m.old_manuscripts)
                             ),
                             DEFAULT_COMMANDS)

NORTHERN_MEADOW = Location("PratoDelNord",
                           m.northern_meadew,
                           LocationList(EASTERN_MOUNTAINS),
                           ItemList(
                               Item("Pony", m.pony)
                           ),
                           DEFAULT_COMMANDS)

HOME = Location('Casa',
                m.home_message,
                LocationList(WESTERN_FOREST, NORTHERN_MEADOW),
                ItemList(
                    Item('LetteraDiBenvenuto', m.welcome_letter)
                ),
                DEFAULT_COMMANDS)



"""
You speak with the old man. He greets you warmly as if you were old friends. You feel at ease with him. 
"Hello adventurer! Top of the morning to you! You seem like a young and energetic explorer. If you're brave enough, 
your destiny awaits within this cave. That destiny will manifest itself as a portal. Enter this portal and begin the 
next chapter of your life." 
The old man sees the shock on your face and smiles a comforting smile, "I am but a fragile old man, and cannot 
accompany you through this cave, but what I can provide are a few simple spells that will help you along your way. 
Just read my old manuscripts and tryout those spells." 
"""






if __name__ == '__main__':
    from json import dumps
    from os import system
    with open("structure.json", 'w') as structure:
        structure.write(dumps(HOME.get_structure()))
    system("atom structure.json")
        