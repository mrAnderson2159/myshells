import os
import sys
from statistics import mean
from sys import argv
from re import match
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from colors import c_yellow

e = c_yellow('Inserisci il range di valori v_0:v_1 e poi i valori uno dopo l\'altro')
assert len(argv) >= 3 and match(r'^\d+:\d+$', argv[1]) is not None and all(map(str.isdigit, argv[2:])), e

value_range, *values = argv[1:]

values = tuple(map(int, values))
n = len(values)
media = mean(values)
start, stop = map(int, value_range.split(':'))

variations = {'max_len': 0}

print(f'\n{media=}\n')

for i in range(start, stop + 1):
    variation = round((i - media) / (n + 1))
    if variation not in variations:
        variations[variation] = [i]
    else:
        variations[variation].append(i)
    variations['max_len'] = max(len(str(variations[variation])), variations['max_len'])

print(f'Capacità di variazione\tValori{" " * (variations["max_len"])}Nuova media')
for variation, values in variations.items():
    if variation != 'max_len':
        s = f'%11d%10s\t%s%s %8d'
        if not int(variation):
            s = c_yellow(s)
        print(s % (variation, '', str(values), ' ' * (variations["max_len"] - len(str(values)) + 4),
                   media + int(variation)))

