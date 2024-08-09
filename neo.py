import sys, os
from time import sleep
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from debug import debug

if len(sys.argv) > 1 and sys.argv[1] == '--edit':
    os.system(f'atom {__file__}')

clear =  lambda: os.system('clear')

def typewrite(text:str, time:float)  ->  None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(time)

def cl_decorator(func):
    def wrapper(*args, **kwargs):
        clear()
        func(*args, **kwargs)
        sleep(3)
    return wrapper

@cl_decorator
def compose_line(words:str, times:tuple):
    words = words.split(' ')
    for i in range(len(words) - 1, 0, -1):
        if words[i] != '__':
            words.insert(i, ' ')
    e = f'Words and times must have the same length (words: {len(words)}, times: {len(times)})'
    assert len(words) == len(times), e

    for word, time in zip(words, times):
        typewrite(word,time) if word != '__' else sleep(time)

clear()
sleep(2)
compose_line('Wake up __ Neo...', (.08, .2, .3, .5, .2, .15))
compose_line('The __ Matrix __ has you', (.2, .1, .2, .2, .1, .15, .15, .15, .15))
compose_line('Follow the white rabbit',(.05, .05, .05, .05, .05, .05, .05))
os.system('cmatrix')
clear()
