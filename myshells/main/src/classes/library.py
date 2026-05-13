class Library:
    def __init__(self, type:str, name:str, flag:str, above:set, in_main:set=set(), **kwargs):
        self.name = name # intestazione della libreria
        self.flag = flag # carattere alfabetico con cui riferirsi alla libreria
        self.above = above # set di elementi da inserire all'inizio del file
        self.in_main = in_main # set di elementi da inserire dentro la funzione main
        self.standard_main = "int main() {" if not "main" in kwargs else kwargs["main"] # configurazione della funzione main
        self.standard_include = str() # libreria da includere di default
        self.type = type # linguaggio del file

    def body(self) -> str:
        # formazione del corpo del file, viene innanzitutto inclusa la libreria di default
        # dopodiche vengono aggiunti gli elementi spcificati in self.above
        # quindi quelli specificati in self.in_main
        result = self.standard_include +  '\n'.join(self.above) + '\n\n'
        result += self.standard_main + '\n\t' + '\n\t'.join(self.in_main) + '\n\n' + '}'
        return result

    def info(self) -> str:
        # restituisce una descrizione della libreria relativamente al flag
        # in modo tale da poterla indicare nella funzione src.functions.tools.usage()
        message = f"-{self.flag}: create a new file.{self.type} with {self.name}"
        if len(self.in_main):
            message += f" and {' '.join(self.in_main)} inside main function"
        return message

    @classmethod
    def merge_and_get_body(cls, libraries: list) -> str:
        # prende una lista di librerie e unisce in un due set tutti i dati comuni
        # in above e in in_main quindi crea una nuova libreria basata su questi
        # due parametri e ne ritorna il body
        if len(libraries) == 1:
            return libraries[0].body()
        for i in range(1, len(libraries)):
            assert libraries[i - 1].type == libraries[i].type, f"Each library must belong to the same programming language: {libraries[i - 1].name} belongs to {libraries[i - 1].type} and {libraries[i].name} belongs to {libraries[i].type}"
        type = libraries[0].type
        above = set()
        in_main = set()
        for library in libraries:
            above |= library.above
            in_main |= library.in_main

        args = [None, None, above, in_main]
        return (C_Library if type == "c" else Cpp_Library)(*args).body()

class C_Library(Library):
    def __init__(self, name:str, flag:str, above:set, in_main:set=set(), **kwargs):
        super().__init__("c", name, flag, above, in_main)
        self.standard_include = '#include <stdio.h>'

class Cpp_Library(Library):
    def __init__(self, name:str, flag:str, above:set, in_main:set=set(), **kwargs):
        main = 'using namespace std;\n\nint main(int argc, char const *argv[]) {'
        super().__init__("c++", name, flag, above, in_main, main=main)
        self.standard_include = '#include <iostream>'
