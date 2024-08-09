from voice_recognition import Recognizer
from os import system
from colors import *
import subprocess, re, sys


choices = [None,None,None,None,None]
phrase_time_limit = bool(sys.argv[1]) if len(sys.argv) > 1 else True

def copy(output):
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print('\x1b[31m\t'+output+'\x1b[0m')

def parse_date(date:str) -> str:
    months = [
        'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio',
        'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'
    ]
    dmy = date.split(' ')
    month = dmy[1]
    try:
        month = int(month)
    except:
        month = months.index(month) + 1
    finally:
        return f'{dmy[0]}/{month}/{dmy[2]}'

def parse_pay(pay:str) -> str:
    return '?' if re.search(r'non', pay) else '!'

def auto(phrase_time_limit:bool) -> bool:
    while True:
        say("Pronuncia tutto il titolo")
        res = listen(15 if phrase_time_limit else None)
        try:
            if re.search(r'manuale?', res):
                return True
            print(res)
            pagato = re.search(r'non pagata?o?|pagata?o?', res)
            global choices
            choices[0] = res[:pagato.start()]
            choices[1] = re.search(r'di (.+) del', res).group(1)
            choices[2] = pagato.group(0)
            choices[3] = re.search(r'del (.+) descrizione',res).group(1)
            choices[4] = res[re.search(r'descrizione',res).end():]
            choices = [x.strip() for x in choices]
            return False
        except Exception as e:
            red(e)

def manual(phrase_time_limit:bool):
    for i, type in enumerate(types):
        say(type)
        choices[i] = None
        while choices[i] == None:
            choices[i] = listen(3 if phrase_time_limit else None)
            if choices[i] == None:
                red("Non ho capito, puoi ripetere?")
        print(f'{type}: {choices[i]}')

say = lambda s: system(f'say {s}')
listen = Recognizer.listen
types = ['Tipo documento', 'Utente', 'Stato Pagamento', 'Data', 'Descrizione']


'[@tipo documento]-[&utente]-[?/!stato pagamento]-[data gg/mm/aa]-[%descrizione]'

say("Cominciamo")
while True:
    man = auto(phrase_time_limit)
    if man:
        manual(phrase_time_limit)

    copy(f"@{choices[0]}-&{choices[1]}-{parse_pay(choices[2])}-{parse_date(choices[3])}-%{choices[4]}")

    say("Desìderi procedere?")
    go = ''
    while go != 'no' and go != 'sì':
        go = listen(2 if phrase_time_limit else None)
        print(go)
    if go == 'no':
        break
