"""
Introduction
============
This program is for creating a daily todo
list made of fixed obligations which
will be charged automatically and costume obligations which can be added from the
user from time to time.
Every day, at a fixed hour, the program will tell the printer to print the todo
list for that day.

Classes
=======

class Todo
----
This class is used to instantiate an object representing a task to be executed.

Attributes
~~~~~~~~~~
* *fixed* or *occasional* **frequency**
* **task description**
* **day** number
* **date** *pointer*

Methods
~~~~~~~
* **rename** the *task description*
* **day comparison** *methods*
* **object equals** *method*

class DayList
-------
This class is used to instantiate a list to represent the days with not fixed-only todos.

Attributes
~~~~~~~~~~
* empty **list**

Methods
~~~~~~~
* **insert** a todo basing on `Todo.day` comparison
* **find** a todo basing on `Todo.day` binary search
* **change** the `Todo.day` and `Todo.day_pointer` to this list
* **delete** todo from this list

class TodoList
--------
This class has the duty to print out the todos of the day merging fixed and occasional todos.

Attributes
~~~~~~~~~~
* **DayList** containing occasional todos
* **DatabaseManager** a database object to manage data
* **current year day**
* **current week day**
* **last print day** to check whether if the todolist has been printed or not during the day

Methods
~~~~~~~
* **switch printed flag** set the flag to true when the todolist gets printed,
    set to false between midnight and 8am if not already false
* **

"""

from src.settings import STDIN
from src.classes.menus import *
from src.classes.todo_list import TodoList
from os import system
from utils import confirm
from textwrap import dedent


def clear():
    system("clear")


def std_input(prompt: str = '', autoclear: bool = True, **kwargs) -> str:
    if autoclear:
        clear()
    return STDIN(str, dedent(prompt), **kwargs)


def main():
    todo_list = TodoList("src/database/database.json", False)
    while True:
        match main_menu():
            case "print_today_list":
                todo_list.print_today_list()
                input()
            case "print_someday_list":
                data = std_input("In questo menù puoi inserire la data di un giorno di cui vuoi stampare gli "
                                 "appuntamenti.\nSe inserisci un intero questo verrà processato come un giorno "
                                 "del mese corrente se è compreso tra la data di oggi e l'ultimo giorno di questo mese,"
                                 " verrà interpretato come giorno del mese prossimo se è minore della data attuale "
                                 "o verrà considerato come giorno assoluto se è compreso tra l'ultimo "
                                 "giorno di questo mese e 366.\nSe viene aggiunto anche il mese (gg-mm), "
                                 "verrà considerato dell'anno dell'anno attuale se il mese è maggiore o uguale "
                                 "rispetto al mese corrente, in alternativa può essere inserita "
                                 "la data completa (gg-mm-aaaa).\n\nInserisci la data:")
                day = todo_list.process_string_date(data)
                todo_list.print_day_list(day)
                input()
            case "add_todo":
                task = std_input("Scrivi la descrizione del nuovo impegno o \"exit\" per annullare")
                if task != "exit":
                    match add_todo_menu(task):
                        case "fixed":
                            day = add_fixed_todo_day_menu()
                            rep = std_input("Inserisci ogni quanti giorni deve ripetersi l'impegno: "
                                            "scrivi 0 per annullare tutto,\n"
                                            "un numero positivo per rappresentare un intervallo di tempo,\n"
                                            "oppure più numeri separati da spazi "
                                            "se si tratta di una ripetizione irregolare:\n")
                            rep = todo_list.process_repetition(rep)
                            clear()
                            if confirm(f"{task} ogni {', '.join(map(str, rep))} giorni a partire da {Time.DAYS[day]}, "
                                       f"va bene così"):
                                todo = todo_list.add_fixed(task, day, rep)
                                print(f"L'impegno \"{todo}\" è stato aggiunto alla lista degli impegni fissi")
                                input()
                        case "occasional":
                            data = std_input("""
                            In questo menù puoi inserire la data del giorno in cui registrare l'appuntamento.
                            
                            Se inserisci un intero, questo verrà processato come un giorno del mese corrente se 
                            è compreso tra la data di oggi e l'ultimo giorno di questo mese; 
                            verrà interpretato come giorno del mese prossimo se è minore della data attuale;
                            infine, verrà considerato come giorno assoluto se è compreso tra 
                            l'ultimo giorno di questo mese e 366.
                            Se viene aggiunto anche il mese (gg-mm), verrà considerato dell'anno attuale se 
                            il mese è maggiore o uguale rispetto al mese corrente, 
                            in alternativa può essere inserita la data completa (gg-mm-aaaa).
                            """)
                            day = todo_list.process_string_date(data)
                            repetition = std_input("Inserisci ogni quanti giorni deve ripetersi l'impegno:\n"
                                            "un numero non negativo per rappresentare un intervallo di tempo,\n"
                                            "oppure più numeri separati da spazi "
                                            "se si tratta di una ripetizione irregolare:\n")
                            rep = todo_list.process_repetition(repetition)
                            if rep[0]:
                                cnf_msg = f"{task} ogni {', '.join(map(str, rep))} giorni a partire da {day}"
                            else:
                                cnf_msg = f"{task} il {day} senza ripetizioni"
                            if confirm(cnf_msg + ", va bene così"):
                                todo = todo_list.add_occasional(task, day, rep)
                                print(f"L'impegno \"{todo}\" è stato aggiunto alla lista degli impegni occasionali")
                                input()
            case "mod_todo":
                match mod_todo_menu():
                    case "rename":
                        pass
                    case "mod_date":
                        pass
                    case "mod_rep":
                        pass
            case "del_todo":
                match del_todo_menu():
                    case "fixed":
                        pass
                    case "occasional":
                        pass
            case "show_calendar":
                input()
            case _:
                break


if __name__ == "__main__":
    main()
    # print(del_todo_menu.cases)
    # t = TodoList("src/database/database.json")
    # t.print_today_list()
