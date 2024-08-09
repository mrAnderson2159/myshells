# __all__ = ["main_menu", "add_todo_menu", "del_todo_menu", 'mod_todo_menu']

from menu import Menu
from src.settings import STDIN
from src.interfaces.time import Time

__SETTINGS = {'return_value': True, 'stdin': STDIN, "raise_ex_on_exit": False}


def __StandardMenu(name: str, **kwargs) -> Menu:
    kwargs |= __SETTINGS
    return Menu(name, **kwargs)


main_menu = __StandardMenu("Menu principale") \
    .add_item("print_today_list", "Stampa la lista di cose da fare oggi") \
    .add_item("print_someday_list", "Stampa la lista di cose da fare un giorno a scelta") \
    .add_item("add_todo", "Segna un nuovo impegno") \
    .add_item("mod_todo", "Modifica un impegno") \
    .add_item("del_todo", "Elimina un impegno") \
    .add_item("show_calendar", "Visualizza il calendario")

def add_todo_menu(name: str) -> Menu:
    menu = __StandardMenu(f'Scegli la modalità del nuovo impegno "{name}"') \
    .add_item("fixed", "Impegno fisso") \
    .add_item("occasional", "Impegno occasionale")
    return menu()

mod_todo_menu = __StandardMenu("Modifica un impegno") \
    .add_item("rename", "Rinomina un impegno") \
    .add_item("mod_date", "Modifica la data di un impegno") \
    .add_item("mod_rep", "Modifica la frequenza di un impegno")

del_todo_menu = __StandardMenu("Elimina un impegno") \
    .add_item("fixed", "Impegno fisso") \
    .add_item("occasional", "Impegno occasionale")

add_fixed_todo_day_menu = __StandardMenu("Seleziona un giorno della settimana")
for i, day in enumerate(Time.DAYS):
    add_fixed_todo_day_menu.add_item(i, day)

