from typing import *
from os import system
from src.game_item import GameItem
from src.item import Item
from src.keyboard import Keyboard
from src.lists import GameItemList, LocationList, ItemList

class Location(GameItem):
    COMMAND_ARGS = {
        'cd': True,
        'clear': False,
        'help': False,
        'less': True,
        'ls': True,
        'man': True,
        'mv': True,
        'pwd': False
    }

    COMMANDS = []

    def __init__(self, name: str, 
                 message: Callable[[], None],
                 locations: LocationList,
                 items: ItemList,
                 allowed_commands: set[str],
                 *,
                 is_accessible: bool = True,
                 is_resettable: bool = False):
        super().__init__(name)
        self._initial_state = {key: (value.copy() if hasattr(value, 'copy') else value)
                               for key, value in locals().items() if key != 'self'}
        self.message = message
        self.locations = locations
        self.items = items
        self.allowed_commands = allowed_commands
        self.parent: "Location" = None
        self.is_accessible = is_accessible
        self.is_resettable = is_resettable

        for location in locations:
            location.parent = self

    def reset(self):
        if self.is_resettable:
            for key, value in self._initial_state.items():
                print(f'debug:_initial_{key} = {value}, id = {id(value)}')
                print(f'debug:_actual_{key} = {getattr(self, key)}, id = {id(getattr(self, key))}')
                setattr(self, key, value)
                print(f'debug:_after_change_{key} = {getattr(self, key)}\n')

    def pwd(self):
        print(f'Ti trovi in "{self.name}"\n')

    def ls(self):
        print("\n"
              "  Luoghi:")
        for location in self.locations:
            print(f"- {location}")
        print("  Oggetti:")
        for item in self.items:
            print(f"- {item}")
        print()

    def keyboardChoices(self) -> tuple[str]:
        return tuple(map(str, [*self.locations, *self.items]))

    def start(self, *, show_msg: bool = True):
        if show_msg:
            self.message()
        k = Keyboard(self.COMMAND_ARGS, self.allowed_commands, self.keyboardChoices(), self.COMMANDS)
        while True:
            command, *args = k.input().strip().split(' ')
            if command in self.allowed_commands:
                match [command, *args]:
                    case ['pwd']:
                        self.pwd()
                    case ['ls']:
                        self.ls()
                    case ['ls', arg]:
                        if arg in self.locations:
                            self.locations[arg].ls()
                        else:
                            print(f"{arg} non è un oggetto valido da osservare")
                    case ['cd'] | ['cd', '~']:
                        home = self
                        while home.parent is not None:
                            home = home.parent
                        home.start()

                        return
                    case ['cd', '.']:
                        self.message()
                    case ['cd', '..']:
                        parent = self
                        if parent.parent is not None:
                            parent = self.parent
                        self.reset()
                        parent.start()
                        return
                    case ['cd', loc]:
                        if loc in self.locations:
                            location = self.locations[loc]
                            if location.is_accessible:
                                self.reset()
                                location.start()
                                return
                            else:
                                location.message()
                        else:
                            print(f"Non c'è nessuna stanza chiamata {loc}")
                    case ['clear']:
                        system('clear')
                    case ['help']:
                        print("Disponibilità:")
                        for command in self.allowed_commands:
                            print('- ' + command)
                    case ['less']:
                        print("Devi dirmi quale oggetto vuoi osservare con il comando less")
                    case ['less', arg]:
                        if arg in self.items:
                            self.items[arg].less()
                        else:
                            print(f"Non c'è nessun oggetto chiamato {arg} qui")
                    case ['mv'] | ['mv', _]:
                        print('Devi muovere un oggetto A ad una posizione B. Usa "mv OGGETTO_A POSIZIONE_B')
                    case ['mv', object, position]:
                        if object in self.items and position in self.locations:
                            item: Item = self.items[object]
                            location: Location = self.locations[position]
                            location.items.append(item)
                            del self.items[object]
                            k.update(choices=self.keyboardChoices())
                            print(f"{object} spostato in {position}")
                        else:
                            print("Servono un oggetto e una posizione validi per effettuare lo spostamento")
                    case _:
                        print("Il comando inserito non è valido")
            elif command == 'ABORT':
                exit()
                return
            else:
                print(f"Il comando '{command}' non è presente nella stanza '{self.name}'")

    def get_structure(self) -> dict:
        result = {}
        for location in self.locations:
            result[str(location)] = Location.get_structure(location)
        result["items"] = [item for item in map(str, self.items)]
        return result


if __name__ == '__main__':
    EMPTY = Location("", lambda:None, LocationList(), ItemList(),  {""})
