import os
from src.functions.tools import builder

def edit() -> None:
    # apre in atom la cartella del programma
    main_folder = '/'.join(os.path.dirname(__file__).split('/')[:-2])
    os.system(f"open -a 'Visual Studio Code' {main_folder}")

def info(usage: callable) -> None:
    # stampa il "manuale" del programma
    print(usage())

def c(flag_libraries: str, filename_list: list) -> None:
    # crea un file .c
    builder('c', flag_libraries, filename_list)

def cpp(flag_libraries: str, filename_list: list) -> None:
    # crea un file .cpp
    builder('c++', flag_libraries, filename_list)
