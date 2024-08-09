from re import search, finditer


def ffx_cap(string:str, all_sentence:bool = True) -> str:
    '''
        Turns the first letter of a sentence or the first letter of each word inside
        a sentence in upper case.

    :param string: the sentence to convert
    :type string: str
    :param all_sentence: [Optional] True by default it tells if convert the whole sentence
                          or just the first letter of the sentence
    :type all_sentence: bool
    :return: returns the modified string
    :rtype: str
    '''
    if not all_sentence:
        return string.capitalize()
    words = string.split(' ')
    for i in range(len(words)):
        w = words[i]
        j = 0
        try:
            while not w[j].isalpha():
                j += 1
            if j:
                words[i] = w[:j] + w[j].upper() + w[j+1:].lower()
            else:
                words[i] = w[j].upper() + w[j+1:].lower()
        except IndexError:
            continue
    return ' '.join(words)


def camel_split(word:str) -> str:
    '''
        Splits camel-cased words.

    :param word: aCamelCasedWord
    :type word: str
    :return: a Camel Cased Word
    :rtype: str
    '''
    if not search(r'[a-z][A-Z]', word):
        return word
    humps = finditer(r'[a-z][A-Z]', word)
    indexes = [0, *[hump.span()[0] + 1 for hump in humps], len(word)]
    words = []

    for i in range(len(indexes) - 1):
        start, stop = indexes[i], indexes[i + 1]
        words.append(word[start : stop])

    return ' '.join(words)


def int_guil(guil:str) -> int:
    return int(''.join(guil.split('.')))