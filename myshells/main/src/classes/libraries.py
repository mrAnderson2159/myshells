from src.classes.library import *

class Libraries:
    # la lista di tutte le librerie create tramite le classi di src.classes.library
    LIBRARIES = { "c": list(), "c++": list() }

    @classmethod
    def find(cls, type: str, flag: str) -> Library:
        # restituisce una libreria cercata tramite il linguaggio e il flag, None se non la trova
        try:
            return [lib for lib in cls.LIBRARIES[type] if lib.flag == flag][0]
        except IndexError:
            return None

    @classmethod
    def flags(cls) -> dict:
        # restituisce un dizionario contenente come chiavi i linguaggi e come valori
        # una stringa composta da tutti i flag delle librerie in quel linguaggio.
        # La funzione è pensata per essere utilizzata da src.functions.tools.usage()
        mydict = {'c':'-_', 'c++':'-_'}
        for lang in cls.LIBRARIES:
            for lib in cls.LIBRARIES[lang]:
                mydict[lang] += lib.flag
        return mydict

    @classmethod
    def newLib(cls, type: str, name: str, flag: str, above: set = set(), in_main: set = set(), **kwargs):
        # permette di aggiungere una nuova libreria in LIBRARIES
        constructor_args = list(locals().values())[2:] # salva gli argomenti di questa funzione da name in poi
        if not constructor_args[-1]: # elimina i **kwargs se vuoti
            constructor_args.pop()
        cls.LIBRARIES[type].append((C_Library if type == 'c' else Cpp_Library)(*constructor_args))


# C
Libraries.newLib("c", "stdio.h", "n"),
Libraries.newLib("c", "stdio.h", "l", {"#include <stdlib.h>"}, {"system(\"clear\");"}),
Libraries.newLib("c", "time.h", "t", {"#include <time.h>"}),
Libraries.newLib("c", "time.h", "r", {"#include <time.h>"}, {"srand(time(NULL));"}),
Libraries.newLib("c", "unistd.h", "u", {"#include <unistd.h>"}),
Libraries.newLib("c", "math.h", "m", {"#include <math.h>"}),
Libraries.newLib("c", "string.h", "s", {"#include <string.h>"})
Libraries.newLib("c", "ctype.h", "c", {"#include <ctype.h>"})

# C++
Libraries.newLib("c++", "iostream", "n"),
Libraries.newLib("c++", "iostream", "l", set(), {"system(\"clear\");"}),
Libraries.newLib("c++", "string", "s", {"#include <string>"}),
Libraries.newLib("c++", "ctime", "c", {"#include <ctime>"}),
Libraries.newLib("c++", "iomanip", "i", {"#include <iomanip>"})
