import os
import sys
from typing import *

from src.database import Database
from src.v_tree import VTree
from src.v_node import VNode
from src.globals import STDIN

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from menu import Menu
from colors import *
from utils import clear
from switch import Switch


class MainMenu:
    def __init__(self, name: str, database: Database):
        self.db = database
        self.menu = Menu(name, stdin=STDIN)
        self.current_queue: Union[VTree, None] = None
        self.build()

    def test(self):
        pass

    @staticmethod
    def feature(name: str):
        clear()
        cyan(name + '\n')

    @staticmethod
    def ask(data: str):
        return STDIN(str, f'Hai inserito {data}\nva bene così? (y/n)', 1).strip() == 'y'

    def get_list(self, feature: str) -> List[str]:
        _list = list()

        def screen():
            self.feature(feature)
            print("Inserisci gli elementi della coda, cancella l'elemento precedente -1 e termina con \"end\"")
            for line in _list:
                print(f'> {line}')

        screen()
        while True:
            current_line = STDIN(str, prefix='> ')
            if current_line == 'end':
                break
            if current_line == '-1':
                _list.pop()
            elif current_line:
                _list.append(current_line)
            screen()
        return _list

    def new_queue(self):
        self.feature('Impostazioni nuova coda')
        control = False
        lt_ph_def = 'Cosa vuoi fare prima?'
        gt_ph_def = 'Cosa vuoi fare dopo?'
        name = lt_ph = gt_ph = str()
        elements = list()
        queue = None

        while not control:
            name = STDIN(str, "Inserisci il nome della coda\n> ")
            lt_ph = STDIN(str,
                f"Inserisci la frase di confronto minore "
                f"(premi invio per mantenere quella di default: "
                f"[{c_yellow(lt_ph_def)}])") or lt_ph_def
            gt_ph = STDIN(str,
                f"Inserisci la frase di confronto maggiore "
                f"(premi invio per mantenere quella di default: "
                f"[{c_yellow(gt_ph_def)}])") or gt_ph_def
            elements = self.get_list('Inserzione elementi nuova coda')
            self.feature('Impostazioni nuova coda')
            control = self.ask(
                f'\n\tnome: {name}\n\tconfronto maggiore: {gt_ph}\n\tconfronto minore: {lt_ph}\n\telementi: {elements}')
        control = False
        while not control:
            self.feature('Costruzione nuova coda')
            queue = VTree(name, lt_ph, gt_ph)
            for element in elements:
                queue.insert(element)
            control = self.ask('\n' + str(queue) + '\n')
        q_dict = queue.dict()
        self.db[q_dict.name] = q_dict
        self.db.write()
        self.current_queue = queue
        self.manage_queue()

    def select_queue(self):
        menu = Menu('Selezione coda', return_value=True, stdin=STDIN)
        for queue in self.db.db:
            menu.add_item(queue, queue)
        queue = menu.start()
        if queue:
            queue = self.db[queue]
            queue = VTree().build(queue)
            self.current_queue = queue
            self.manage_queue()

    def manage_queue(self):
        menu = Menu('Gestione coda', return_value=True, print_name=False, auto_clean=False, stdin=STDIN)
        menu.add_item('add', 'Aggiungi un elemento')
        menu.add_item('change', 'Sposta un elemento')
        menu.add_item('rename', 'Rinomina un elemento')
        menu.add_item('exchange', 'Scambia due elementi')
        menu.add_item('exmin', 'Completa il primo elemento')
        menu.add_item('complete', 'Completa un altro elemento')
        menu.add_item('delete', 'Elimina un elemento')
        menu.add_item('show_tree', 'mostra l\'albero')
        menu.add_item('show_hash', 'mostra tabella hash')
        # menu.add_item('move_block', 'Sposta un blocco')

        update_var = None

        def update(node: VNode = None, completed=True):
            name = self.current_queue.name
            if completed:
                self.db[name].completed.append(node.data)
            self.db[name].tree = self.current_queue.dict().tree
            self.db.write()

        def exmin():
            nonlocal update_var
            update_var = m = self.current_queue.extract_min()
            update(m)

        def complete():
            nonlocal update_var
            self.feature('Completa un elemento')
            print('Inserisci il numero dell\'elemento che hai appena completato')
            update_var = d = self.current_queue.ask_delete('\t').node
            update(d)

        def delete():
            self.feature('Elimina un elemento')
            print('Inserisci il numero dell\'elemento che vuoi eliminare')
            self.current_queue.ask_delete('\t')
            update(completed=False)

        def exchange():
            nodes = self.current_queue.in_order()
            ph_a = 'Seleziona il primo elemento'
            ph_b = 'Seleziona il secondo elemento'
            nds: List[VNode, VNode] = [None, None]
            for i, ph in enumerate((ph_a, ph_b)):
                # debug(nds)
                if nds[0]:
                    ph += f' (scambia con {nds[0].data})'
                menu = Menu(ph, return_value=True, stdin=STDIN)
                for node in nodes:
                    menu.add_item(node, node.data)
                nds[i] = menu.start()
                if nds[i] is None:
                    return
            a, b = nds
            self.current_queue.hash_swap(a, b)
            a.exchange_with(b)
            update(completed=False)

        def add():
            self.feature('Aggiungi un elemento')
            name = STDIN(str, 'Inserisci il nome del nuovo elemento')
            if name:
                print(self.current_queue, '\n')
                self.current_queue.insert(name)
                update(completed=False)

        def get_mod_el(phrase: str) -> VTree.HashNode:
            keys = self.current_queue.get_data()
            menu = Menu(phrase, return_value=True, stdin=STDIN)
            for i, key in enumerate(keys):
                menu.add_item((i, key), key)
            index, key = menu.start()
            node = self.current_queue.hash_get_closest(key, index)
            # debug(node)
            return node

        def change():
            node = get_mod_el('Quale elemento vuoi modificare?').node
            id = node.value
            node = self.current_queue.delete(node).node.data
            node = self.current_queue.insert(node).node
            node.value = id
            update(completed=False)

        def rename():
            hash_node = get_mod_el('Quale elemento vuoi rinominare?')
            # return
            index, node = hash_node
            name = STDIN(str, f"Inserisci il nuovo nome che vuoi dare all'elemento \"{node.data}\"")
            self.current_queue.hash_delete(index)
            node.rename(name)
            self.current_queue.hash_put(node)
            update(completed=False)

        def show_tree():
            self.feature(f'Mostra albero')
            print(self.current_queue.root)
            nodes = self.current_queue.in_order()
            size = self.current_queue.size
            # NB: min e max devono essere attributi di istanza
            minimum = self.current_queue.min(self.current_queue.root).priority
            maximum = self.current_queue.max(self.current_queue.root).priority
            for node in nodes:
                # print(f'{node.priority=} {{{node.value}}} {node.data}')
                print('%6.2f\t%5.1f\t%5s\t%s' % (
                    node.probable_index(size, minimum, maximum), node.priority, f'{{{node.value}}}', node.data))
            input()

        def show_hash():
            self.feature(f'Mostra tabella hash')
            for i, node in enumerate(self.current_queue.hash_table):
                if node is not None:
                    print(
                        '%5.1f\t# %4d\t## %3d\t%5s\t%s' % (node.priority, node.hash, i, f'{{{node.value}}}', node.data))
                    # print(f'#{node.hash} ##{i} {{{node.value}}} {node.data}')
            input()

        def move_block():
            nodes = self.current_queue.in_order()
            ph_a = 'Seleziona l\'estremo sinistro del blocco'
            ph_b = 'Seleziona l\'estremo destro del blocco'
            nds: List[VNode, VNode] = [None, None]
            for i, ph in enumerate((ph_a, ph_b)):
                # debug(nds)
                menu = Menu(ph, return_value=True, stdin=STDIN)
                for node in nodes:
                    menu.add_item(node, node.data)
                nds[i] = menu.start()
            lp, rp = map(VNode.get_priority, nds)
            block = self.current_queue.move_block((lp, rp))
            print(block)
            print(self.current_queue.root)
            input()

        while True:
            clear()
            self.feature(f"Gestione coda\n\n{self.current_queue}")
            # print(self.current_queue.root)
            choice = menu.start()
            try:
                with Switch(choice) as s:
                    s.case('exmin', exmin)
                    s.case('complete', complete)
                    s.case('delete', delete)
                    s.case('add', add)
                    s.case('change', change)
                    s.case('rename', rename)
                    s.case('exchange', exchange)
                    s.case('show_tree', show_tree)
                    s.case('show_hash', show_hash)
                    # s.case('move_block', move_block)
            except AssertionError as e:
                if choice is not None:
                    raise e
            except FileNotFoundError:
                yellow("Il nas non è connesso, effettua l'accesso quindi premi invio per salvare le modifiche")
                input()
                if choice in ('complete', 'exmin'):
                    update(update_var)
                else:
                    update(completed=False)
            except TypeError:
                continue
            if not choice:
                break

    def build(self):
        self.menu.add_item('new', 'crea una nuova coda', self.new_queue)
        self.menu.add_item('select', 'seleziona una coda', self.select_queue)
        self.menu.add_item('delete', 'elimina una coda', self.test)

    def __call__(self):
        self.menu.start()
