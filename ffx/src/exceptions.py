class HashTableException(Exception):
    '''Base (catch-all) Hashtable exception.'''

class FullTableException(HashTableException):
    '''Hash table is already full.'''
    def __init__(self, o:'Hashable'):
        super().__init__(f'The hash table for {o} is full')

class ObjectAlreadyStoredException(HashTableException):
    '''User tried to put object with same key of another already stored'''
    def __init__(self, to_be_put:'Hashable', already_existing: 'Hashable'):
        m = f'Cannot put {to_be_put} inside the hash table because it already exists {already_existing} element with same key'
        super().__init__(m)