import  json

class Experimento:
    def __init__(self, dbpath = 'db/experimento.json'):
        self.dbpath = dbpath
        try:
            self.dbload(dbpath)
        except Exception as e:
            print(e)
            self.__new_data()

    def __new_data(self):
        self.data = {
            "attacco": {
                "A": 0,
                "S": 0,
                "Z": 0,
            },
            "difesa": {
                "A": 0,
                "S": 0,
                "Z": 0,
            },
            "speciale": {
                "A": 0,
                "S": 0,
                "Z": 0,
            }
        }

    def dbload(self, dbpath = None):
        if not dbpath:
            dbpath = self.dbpath
        with open(dbpath, 'r') as db:
            self.data = json.loads(db.read())
        return self

    def dbwrite(self, dbpath = None):
        if not dbpath:
            dbpath = self.dbpath
        with open(dbpath, 'w') as db:
            db.write(json.dumps(self.data))
        return self

    def __calc(self):
        calc = {'attacco':[0,'a'], 'difesa':[0,'d'], 'speciale':[0,'s']}
        res = ''
        spaces = lambda x : ' ' * (9 - len(x))
        color = lambda n : f'\x1b[96m38\x1b[0m' if n >= 38 else n
        for tipo in self.data.keys():
            calc[tipo][0] = self.data[tipo]['A'] + self.data[tipo]['S'] * 3 + self.data[tipo]['Z'] * 5
            res += f"{tipo}{spaces(tipo)}: {color(calc[tipo][0])}\n\t"
        return res[:-2]

    def __piece_name(self, tipo, pezzo = ''):
        d = {'a':'attacco','d':'difesa','s':'speciale'}
        art = 'd\'' if tipo == 'a' else ('di ' if tipo == 'd' else '')
        return f'Pezzo {art}{d[tipo]} {pezzo.upper()}'

    def add(self, _str):
        self.__mod(_str, +1)
        print(f"\x1b[93m\"{self.__piece_name(*_str)}\" aggiunto alla collezione\x1b[0m")
        return self

    def delete(self, _str):
        self.__mod(_str, -1)
        print(f"\x1b[93m\"{self.__piece_name(*_str)}\" rimosso alla collezione\x1b[0m")
        return self

    def __mod(self, _str, q):
        assert len(_str) == 2
        tipo, pezzo = _str
        assert tipo in ('a','d','s') and pezzo in ('a','s','z')
        d = {'a':'attacco','d':'difesa','s':'speciale'}
        old_val = self.data[d[tipo]][pezzo.upper()]
        art = 'd\'' if tipo == 'a' else ('di ' if tipo == 'd' else '')
        if old_val + q < 0:
            raise ArithmeticError(f"\x1b[31mIl \"pezzo {art}{d[tipo]} {pezzo.upper()}\" si trova già a 0\x1b[0m")
        self.data[d[tipo]][pezzo.upper()] += q

    def __repr__(self):
        res = '\nExperimento(\n'
        for i, tipo in enumerate(self.data.keys()):
            for pezzo in self.data[tipo].keys():
                res += '\tPezzo '
                if tipo == 'attacco':
                    res += 'd\'attacco '
                elif tipo == 'difesa':
                    res += 'di difesa '
                else:
                    res += tipo + ' '
                res += f'{pezzo}: {self.data[tipo][pezzo]}\n'
            if i != 2:
                res += '\n'
        res += '\n\t' + self.__calc() + '\n'
        return res + ')\n'

    def p(self):
        print(self)
        return self
