from os import system
from random import randint
from time import sleep
from sys import stdout



punti = ['sasso', 'carta', 'forbice']
match = ['Ha vinto il computer', 'È finita in parità', 'Hai vinto!']

def get_match(player:int, computer:int) -> str:
    return match[(2*computer + player + 1) % 3]

def print_function(string:str, timeout:float=0.):
    stdout.write(string)
    stdout.flush()
    if timeout:
        sleep(timeout)

def wrong():
    print_function("\nLa scelta inserita non è valida, premi invio ")
    input()

def suspance(time:float = .5):
    print_function("\nIl computer gioca")
    for i in range(3):
        sleep(time)
        print_function('.')
    sleep(time)

def result(player:int, computer:int, timeout:float=2.):
    print_function(f" {punti[computer]}! ", timeout)
    print_function(f"\n\n{get_match(player, computer)} ", timeout)

def play():
    wanna_play = True
    try:
        while wanna_play:
            system('clear')
            computer = randint(0,2)
            try:
                player = int(input("Scegli:\n\t1. sasso\n\t2. carta\n\t3. forbice\n> ")) - 1
                if not 0 <= player <= 2:
                    raise ValueError
            except ValueError:
                wrong()
                continue
            suspance()
            result(player, computer)
            wanna_play = input("\n\nVuoi fare un'altra partita? (y/N): ") == 'y'
    except KeyboardInterrupt:
        pass

play()




# Spiegazione get_match
# ==============================================================================
# I giocatori possono giocare
#
#                   (sasso, carta, forbice) = (0, 1, 2),
#
# e l'esito di un match può essere
#
#                   (sconfitta, parità, vittoria) = (0, 1, 2)
#
# Consideriamo l'esito rispetto al player e costruiamo una tabella che incrocia
# la giocata del player (colonna) con la giocata del computer (riga), calcolando
# l'esito
#                           |   0   1   2
#                       -------------------
#                       0   |   1   0   2
#                       1   |   2   1   0
#                       2   |   0   2   1
#
# Considerando la matrice a coefficienti in Z_3 degli esiti, possiamo scrivere
# i tre vettori riga come combinazioni lineari dei vettori (1 0 2) e (1 1 1)
#
# v_0 = (1 0 2) = ((1 0 2) + 0(1 1 1))  (mod 3)
# v_1 = (2 1 0) = ((1 0 2) + 1(1 1 1))  (mod 3)
# v_2 = (0 2 1) = ((1 0 2) + 2(1 1 1))  (mod 3)
#
# Possiamo notare che lo scalare che moltiplica il vettore (1 1 1) per ogni
# giocata p del player è proprio p, quindi in generale
#
#                   v_p = ((1 0 2) + p(1 1 1))  (mod 3)
#
# Poiché del generico v_p siamo interessati all'incrocio con la scelta c del
# computer, l'esito è dato da v_p[c], quindi
#
#                   e = v_p[c] = (((1 0 2) + p(1 1 1))  (mod 3))[c]
#
# È dimostrabile che l'accesso ad un elemento di un vettore è distributivo
# rispetto alla somma, pertando
#
#                   e = ((1 0 2)[c] + p(1 1 1)[c])  (mod 3)
#
# da cui ricaviamo la formula finale
#
#                   e = ((1 0 2)[c] + p)  (mod 3)
#
# se però notiamo che (1 0 2) = ((0 1 2) + (1 2 3))  (mod 3) e se consideriamo
# che la scelta c del computer è (0 1 2) = (c c c) e che (1 2 3) = (0 + 1, 1 + 1, 2 + 1)
# possiamo anche dire che (1 2 3) = (c + 1, c + 1, c + 1), ma allora
# la scelta del computer è
#   (1 0 2) = (0 1 2) + (1 2 3) = (c c c) + (c + 1, c + 1, c + 1) = (2c + 1, 2c + 1, 2c + 1)
# a questo punto la prendiamo una sola volta e sostituiamo nell'equazione precedente
# ottenendo
#
#                   e = (2c + p + 1)  (mod 3)
