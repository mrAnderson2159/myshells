import math
import os
import sys
from typing import *

from src.globals import STDIN
from src.phrasal_v_node import PhrasalVNode
from src.v_node import VNode
from src.v_tree_dict import VTreeDict

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from utils import swap


class VTree:
    def __init__(self, name: str = None,
                 lt_phrase: str = None,
                 gt_phrase: str = None,
                 hash_table_size: int = 257
                 ) -> None:
        self.size: int = 0
        self.name: str = name
        self.count: int = 0
        self.root: Union[VNode, None] = None
        self.create_node: PhrasalVNode = PhrasalVNode(lt_phrase, gt_phrase)
        self.HTS: int = hash_table_size
        self.hash_table: List[Union[VNode, None]] = [None] * self.HTS
        self.priority_range: Tuple[float, float] = (0, hash_table_size - 1)

    class HashNode:
        def __init__(self, index: int, node: VNode):
            self.index = index
            self.node = node

        def __iter__(self):
            for value in (self.index, self.node):
                yield value

        def __str__(self):
            index = self.index
            value = self.node.value
            hash_value = self.node.hash
            priority = self.node.priority
            data = self.node.data
            values = ', '.join([f'{key}={value}' for key, value in locals().items() if key != 'self'])
            return f'HashNode({values})'

        def __repr__(self):
            return str(self)

    def __getitem__(self, key: str) -> List[HashNode]:
        return self.hash_get(key)

    def __str__(self):
        if self.none_root():
            return 'None'
        result = self.get_data()
        return '\n'.join([f'{i + 1}. {data}' for i, data in enumerate(result)])
        # result = self.in_order()
        # return '\n'.join([f'{i+1}. {node.data} {{{node.value}}}' for i, node in enumerate(result)])

    def __repr__(self):
        return str(self.root)

    def dict(self) -> Union[VTreeDict]:
        def init(node: VNode) -> Union[dict, None]:
            if node is None:
                return None
            return {
                'value': node.value,
                'data': node.data,
                'hash': node.hash,
                'left': init(node.left),
                'right': init(node.right)
            }

        result = init(self.root)
        phrases = self.create_node.lt_phrase, self.create_node.gt_phrase
        name = self.name
        return VTreeDict(name, phrases, result)

    def build(self, dict_tree: VTreeDict) -> "VTree":
        self.name = dict_tree.name
        self.create_node = PhrasalVNode(dict_tree.phrases[0], dict_tree.phrases[1])

        def init(dict_tree: dict,
                 priority_interval: Tuple[float, float],
                 count: int = 0
                 ) -> Tuple[Union[VNode, None], int]:
            if dict_tree is None:
                return None, count
            node = self.create_node(dict_tree['value'], dict_tree['data'])
            a, b = priority_interval
            q = (a + b) / 2
            node.set_priority(q)
            count = max(node.value, count)
            left, count = init(dict_tree['left'], (a, q), count)
            self.hash_put(node)
            right, count = init(dict_tree['right'], (q, b), count)
            node.set_left(left)
            node.set_right(right)
            return node, count

        self.root, self.count = init(dict_tree.tree, self.priority_range)
        # debug(self.size)
        return self

    def in_order(self) -> List[VNode]:
        result = []

        def init(node: VNode, result: list, priority_range: Tuple[float, float]) -> None:
            a, b = priority_range
            q = math.floor((a + b) / 2)
            if node.has_left():
                init(node.left, result, (a, q))
            node.set_priority(q)
            result.append(node)
            if node.has_right():
                init(node.right, result, (q, b))

        init(self.root, result, self.priority_range)
        return result

    def set_root(self, node: Union[VNode, None]) -> VNode:
        self.root = node
        if node is not None:
            node.parent = None
        return self.root

    def none_root(self) -> bool:
        return self.root is None

    def height(self) -> int:
        return self.root.height if not self.none_root() else 0

    @staticmethod
    def min(node: VNode) -> Union[VNode, None]:
        if node is None:
            return None

        def init(node: VNode) -> VNode:
            if not node.has_left():
                return node
            return init(node.left)

        return init(node)

    def extract_min(self) -> Union[VNode, None]:
        if self.none_root():
            return None

        minimum = self.min(self.root)

        index = self.hash_index_of(minimum)
        self.hash_delete(index)

        if minimum.is_root():
            self.set_root(None)
            return minimum
        parent = minimum.parent
        parent.detach(minimum)
        self.avlize(self.root)
        return minimum

    @staticmethod
    def max(node: VNode) -> Union[VNode, None]:
        if node is None:
            return None

        def init(node: VNode) -> VNode:
            if not node.has_right():
                return node
            return init(node.right)

        return init(node)

    def avlize(self, node) -> int:
        if node is None:
            return -1
        # debug(f'node: {node.value} {node.data}')
        # debug(self.root)

        if node.has_right() and not node.has_left() and node.right.has_no_children():
            right = node.right
            if node.is_root():
                self.set_root(node.right)
                self.root.set_left(node)
                node.right = None
            else:
                node.swap_with_child(node.right)
            node = right
        lh = self.avlize(node.left)
        rh = self.avlize(node.right)
        dh = abs(lh - rh)
        if dh > 1:
            # debug(f'node: {node.value} {node.data}')
            # debug(f'dh = {dh}')
            # debug(self.root)
            node = self.rebalance(node, lh, rh)
            self.avlize(node)
        return node.height

    def rebalance(self, tree, lh, rh) -> VNode:
        z = tree
        p = z.parent

        if lh >= rh:
            y = z.left
        else:
            y = z.right
        if y.left and y.right:
            if y.left.height > y.right.height:
                x = y.left
            elif y.left.height < y.right.height:
                x = y.right
            else:
                if y == z.left:
                    x = y.left
                else:
                    x = y.right
        elif y.left:
            x = y.left
        else:
            x = y.right

        single_rotation = (y == z.left and x == y.left) or (y == z.right and x == y.right)

        if single_rotation:
            if p is not None:
                if z == p.left:
                    p.set_left(y)
                else:
                    p.set_right(y)
            else:
                self.set_root(y)
            if y == z.left:
                z.set_left(y.right)
                y.set_right(z)
            else:
                z.set_right(y.left)
                y.set_left(z)
            tree = y
        else:
            if p is not None:
                # debug(f'p = {p.value} {p.data}')
                if z == p.left:
                    p.set_left(x)
                else:
                    p.set_right(x)
            else:
                # debug('p is None, root change')
                self.set_root(x)

            t1 = x.left
            t2 = x.right

            if x == y.left:
                x.set_left(z)
                x.set_right(y)
                z.set_right(t1)
                y.set_left(t2)
            else:
                x.set_left(y)
                x.set_right(z)
                y.set_right(t1)
                z.set_left(t2)
            tree = x
            # debug(f'x = {x.value} {x.data}, root = {self.root.value} {self.root.data}')
        return tree

    ''' Algorithm move-block
    
        1.  Ottenere i due nodi estremi del blocco e ricavare le loro priorità per ottenere un range
            
        2.  L'algoritmo restituisce due alberi: in_root e in_block. L'albero in_root diventerà la 
            radice dall'avl, l'albero in_block sarà il blocco cercato. L'algoritmo prende in input un 
            un nodo e il range, quindi esegue i seguenti passaggi
            
            a. Definisce una classe block con attributi in_block e in_root
            
            b. Definisce una funzione init con i seguenti passaggi
                I. Se il nodo non ha figli ed è nel range, restituisce se stesso in_block e None in_root,
                   altrimenti restituisce se stesso in_range e None in block
                   
                II. Altrimenti se è nel range chiama ricorsivamente i figli, fa il merge dei loro
                    in_root e restituisce se stesso in_block e il merge in_root
                    
                III. Altrimenti se è un estremo del range salva il figlio esterno al range in una variabile, 
                     chiama ricorsivamente il figlio interno da cui estrae l'in_root e l'in_block, 
                     pone l'in_block al posto del figlio interno e fa il merge dell'in_root col figlio
                     esterno, quindi restituisce i due alberi
                     
                IV. Altrimenti se è esterno al range, ricava l'in_root dal figlio interno, fa il merge con
                    questo in_root e si restituisce come in_root oltre a restituire l'in_block 
                    del figlio interno
                     
            c. Richiama la funzione init sulla radice e il range, fa puntare la radice dell'avl
               all'in_root e restituisce l'in_block
               
            d. Si fa l'avlize sulla radice
            
            e. La chiamante della init usa una speciale funzione insert_block per inserire il
               blocco al posto giusto 
        
        3.  La funzione merge è simile al caso della funzione delete in cui bisogna cancellare 
            un nodo con due figli     
            
        4. La funzione insert_block farà un in_order sulla radice per reimpostare le priorità      
    '''

    def move_block(self, range: Tuple[float, float]) -> VNode:
        def init(node: VNode, range: Tuple[float, float]) -> Tuple[Optional[VNode], Optional[VNode]]:
            '(block, root)'
            lp, rp = range
            priority = node.priority
            left = node.left
            right = node.right
            if node.has_no_children() and lp <= priority <= rp:
                return node, None
            elif node.has_no_children():
                return None, node
            elif lp < priority < rp:
                lb, lr = init(left, range)
                if right is not None:
                    rb, rr = init(right, range)
                else:
                    rb = rr = None
                if lb != left:
                    node.detach(left)
                    node.set_left(lb)
                if rb != right:
                    node.detach(right)
                    node.set_right(rb)
                    # debug(lr)
                    # debug(rr)
                in_root = self.merge(lr, rr)
                # debug(in_root)
                return node, in_root
            elif priority < lp:
                if right is not None:
                    rb, rr = init(right, range)
                    if rr != right:
                        node.detach(right)
                        node.set_right(rr)
                    return rb, node
                return None, node
            elif priority > rp:
                # debug(node)
                lb, lr = init(left, range)
                # debug(lb)
                # debug(lr)
                if lr != left:
                    node.detach(left)
                    node.set_left(lr)
                # debug(node)
                return lb, node
            elif priority == lp:
                node.detach(left)
                _, rr = init(right, range)
                in_root = self.merge(left, rr)
            else:
                node.detach(right)
                _, lr = init(left, range)
                in_root = self.merge(lr, right)
            return node, in_root

        block, root = init(self.root, range)
        # debug(block)
        # debug(root)
        # self.print_status(root)
        self.set_root(root)

        vt = VTree('block', self.create_node.lt_phrase, self.create_node.gt_phrase)
        vt.set_root(block)
        vt.avlize(vt.root)
        self.avlize(root)

        return vt.root

    def print_status(self, node: VNode):
        if node is not None:
            self.print_status(node.left)
            value = node.value
            parent = node.parent.value if node.parent is not None else None
            left = node.left.value if node.left is not None else None
            right = node.right.value if node.right is not None else None
            print(f'{value=} {parent=} {left=} {right=}')
            self.print_status(node.right)

    def merge(self, left: VNode, right: VNode) -> VNode:
        if left is None:
            return right
        if left.right is None:
            # debug(left)
            # debug(right)
            left.set_right(right)
            return left
        root = self.successor(left)
        root.parent.detach(root)
        root.set_left(left)
        root.set_right(right)
        return root

    def insert(self, data: str) -> HashNode:
        self.count += 1
        new_node: VNode = self.create_node(self.count, data.strip())
        new_node.set_priority((self.HTS - 1) / 2)

        index = self.hash_put(new_node).index
        hash_node = self.HashNode(index, new_node)

        if self.none_root():
            self.root = new_node
            return hash_node

        def init(node: VNode, new_node: VNode, priority_range: Tuple[float, float]) -> VNode:
            if node is not None:
                a, b = priority_range
                p = node.priority
                if node.has_no_children():
                    if new_node < node:
                        node.set_left(new_node)
                        b = p
                    else:
                        if node.is_root():
                            self.root = new_node
                            new_node.set_left(node)
                        else:
                            node.set_right(new_node)
                            node.swap_with_child(new_node)
                        a = p
                    q = (a + b) / 2
                    new_node.set_priority(q)
                    self.avlize(self.root)
                    return new_node

                if new_node < node:
                    return init(node.left, new_node, (a, p))

                if not node.has_right():
                    node.set_right(new_node)
                    q = (p + b) / 2
                    new_node.set_priority(q)
                    return new_node

                return init(node.right, new_node, (p, b))

        init(self.root, new_node, self.priority_range)
        return hash_node

    def predecessor(self, node: VNode) -> VNode:
        if node.has_left():
            return self.max(node.left)
        x = node
        y = x.parent
        while y is not None and y.left == x:
            x = y
            y = x.parent
        return y

    def successor(self, node: VNode) -> VNode:
        if node.has_right():
            return self.min(node.right)
        x = node
        y = x.parent
        while y is not None and y.right == x:
            x = y
            y = x.parent
        return y

    def get_data(self) -> List[str]:
        return list(map(lambda node: node.data, self.in_order()))

    def ask_delete(self, pre_char: str = '', sentinel: int = -1) -> HashNode:
        choice = str()
        nodes = self.in_order()
        for i, node in enumerate(nodes):
            print(f'{pre_char}{i + 1}. {node.data}')
        while True:
            try:
                choice = STDIN(int, prefix='> ')
                if choice == sentinel or not choice:
                    break
                choice = int(choice) - 1
                return self.delete(nodes[choice])
            except ValueError:
                print(
                    f"Devi inserire il numero dell'elemento da cancellare, "
                    f"{choice} non è una scelta valida, per favore riprova\n"
                )

    def delete(self, node: VNode) -> HashNode:
        res = node
        if node.has_both_children():
            res = self.create_node(node.value, node.data)
            s = self.successor(node)
            index = self.hash_index_of(s)
            ps = s.parent
            node.value = s.value
            node.data = s.data
            ps.detach(s)
        else:
            if node.has_no_children():
                if node.is_root():
                    self.set_root(None)
                else:
                    node.parent.detach(node)
            elif not node.has_right():
                if node.is_root():
                    self.set_root(node.left)
                else:
                    p = node.parent
                    left = node.left
                    p.detach(node)
                    p.set_left(left)
            index = self.hash_index_of(res)

        self.avlize(self.root)

        res.left = res.right = res.parent = None

        self.hash_delete(index)
        return self.HashNode(index, res)

    def compress(self, node: VNode) -> int:
        return node.hash % self.HTS

    def hash_put(self, node: VNode) -> HashNode:
        i = 0
        index = self.compress(node)
        while self.hash_table[index + i] is not None:
            i += 1
        self.hash_table[index + i] = node
        self.size += 1
        return self.HashNode(index + i, node)

    def hash_get(self, key: str) -> List[HashNode]:
        i = 0
        index = self.compress(VNode(0, key))
        result = list()
        while self.hash_table[index + i] is not None:
            if self.hash_table[index + i].data == key:
                result.append(self.HashNode(index + i, self.hash_table[index + i]))
            i += 1
        return result

    def hash_swap(self, a: VNode, b: VNode) -> None:
        a_index = self.compress(a)
        b_index = self.compress(b)
        for index, node in zip((a_index, b_index), (a, b)):
            i = 0
            while (curr := self.hash_table[index + i]) is not None:
                if curr.data == node.data and curr.value == node.value:
                    index += i
                    break
                i += 1
            if curr is None:
                raise IndexError(f'Node({node.value}, {node.data}) not in hash table')
        self.hash_table[a_index], self.hash_table[b_index] = self.hash_table[b_index], self.hash_table[a_index]

    def hash_get_closest(self, key: str, index: int) -> Union[HashNode, None]:
        items = self.hash_get(key)
        if not len(items):
            return None
        if len(items) == 1:
            return items[0]

        size = self.size
        # Se minimum e maximum fossero attributi di classe, questa funzione avrebbe
        # costo costante, tuttavia a causa di queste due chiamate ha costo log(n)
        minimum = self.min(self.root).priority
        maximum = self.max(self.root).priority

        # debug(locals())

        def init(table: List[VTree.HashNode], p: int, r: int, index: int) -> VTree.HashNode:
            if r - p + 1 > 2:
                q = math.floor((r - p) / 2)
                prev = table[q - 1].node.probable_index(size, minimum, maximum)
                curr = table[q].node.probable_index(size, minimum, maximum)
                # debug(locals())
                if prev < index < curr:
                    if index - prev < curr - index:
                        return table[q - 1]
                    else:
                        return table[q]
                elif index < prev:
                    return init(table, p, q, index)
                else:
                    return init(table, q, r, index)
            else:
                prev = table[p].node.probable_index(size, minimum, maximum)
                curr = table[r].node.probable_index(size, minimum, maximum)
                # debug(locals())

                if index - prev < curr - index:
                    return table[p]
                else:
                    return table[r]

        return init(items, 0, len(items) - 1, index)

    def hash_index_of(self, node: VNode) -> Union[int, None]:
        index = self.compress(node)
        id = node.value
        key = node.data
        i = 0
        while (current := self.hash_table[index + i]) is not None:
            if current.value == id and current.data == key:
                return index + i
            i += 1
        return None

    def hash_rebuild(self, index: int) -> None:
        if self.hash_table[index] is None:
            i = 1
            while self.hash_table[index + i] is not None:
                if self.compress(self.hash_table[index + i]) <= index + i:
                    swap(self.hash_table, index, index + i)
                    index += 1
                    i = 1
                else:
                    i += 1

    def hash_delete(self, index: int) -> VNode:
        node = self.hash_table[index]
        self.hash_table[index] = None
        self.hash_rebuild(index)
        self.size -= 1
        return node
