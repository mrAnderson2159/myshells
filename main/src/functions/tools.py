import os, re
from os.path import splitext, exists
from src.classes.libraries import Libraries
from src.classes.library import Library

def usage():
    # restituisce il "manuale" del programma
    flags = Libraries.flags()
    message = f'usage: [-i, -c, -cpp] [,{flags["c"]}, {flags["c++"]}]'
    message += '\n\tfirst group:'
    message += '\n\t\t-i: show this message'
    message += '\n\t\t-c: create a file with c extension and main function'
    message += '\n\t\t-cpp: create a file with cpp extension and main function'
    message += '\n\tsecond group:'
    message += '\n\t\t-_: insert low dash to separate_name_like_this'
    for lang in Libraries.LIBRARIES:
        for lib in Libraries.LIBRARIES[lang]:
            message += '\n\t\t' + lib.info()
    return message

def check_and_return_args(args: list) -> list:
    # si assicura che siano stati passati almeno 3 argomenti da linea di comando
    err = f'To use -c and -cpp flags you need to provide the library flags and the file name in order to procede\n\n{usage()}'
    assert len(args) > 3, err
    return args[2:]

def file_existing_number(filename: str) -> int:
    # controlla se il nome del file termina già con un numero
    # e restituisce quel numero oppure 0
    try:
        return int(re.search(r"(\d+)$", filename).group(0))
    except AttributeError:
        return 0
    except Exception as e:
        raise e

def builder(lang: str, flag_libraries: str, filename_list: list) -> None:
    # prende la stringa dei flag scelti dall'utente e il nome del file da creare,
    # da ciascuna lettera della stringa crea una src.classes.library.Library
    # e la salva in un array, tramite
    # src.classes.libraries.Libraries.merge_and_get_body() unisce le librerie
    # dell'array e restituisce un body quindi utilizza la funzione create()
    # per creare il file, passando eventualmente un numero già presente alla fine
    # del nome del file
    assert flag_libraries[0] == '-', f"The second argument must one or more {lang} libraries flags\n{usage()}"
    assert lang in ('c', 'c++'), "lang must be c or c++"
    flag_libraries = flag_libraries[1:]
    filename = splitext(('_' if '_' in flag_libraries else ' ').join(filename_list))[0]

    libraries = list()
    for flag in flag_libraries:
        lib = Libraries.find(lang, flag)
        if lib:
            libraries.append(lib)

    body = Library.merge_and_get_body(libraries)
    create(lang, filename, body, file_existing_number(filename))

def create(type: str, filename: str, body: str, number: int = 0) -> None:
    # controlla ricorsivamente se il file esiste gia e, in tal caso, ne aumenta
    # numero finale, una volta creato il titolo di un file che non esiste lo crea
    # e lo apre in atom
    name = f"{filename}{number if number else ''}.{'c' if type == 'c' else 'cpp'}"
    if exists(name):
        create(type, filename, body, number + 1)
    else:
        with open(name, 'a') as f:
            f.write(body)
            os.system(f"atom {name}")
