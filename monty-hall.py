from os import system
from termcolor import colored
from random import choice
from time import sleep
from math import log2
from sys import argv

if len(argv) > 1 and argv[1] == '--edit':
    system(f'atom {__file__}')
    exit(0)

stdout = ''
bits   = 4,2,1

def to_bin(n:int) -> int:
    return int(2 ** (3 - n))

def to_int(b:int) -> int:
    return int(3 - log2(b))

def out_print(suspance:int = 0) -> None:
    system("clear")
    print(stdout)
    if suspance:
        sleep(suspance)

def reset() -> None:
    global stdout
    stdout = "MONTY HALL's PARADOX\n\n"

def append(phrase:str='\n', end='\n', res=False) -> None:
    global stdout
    if res:
        reset()
    stdout += phrase + end

def display(prize:int = 0, visibility:int = 0, user_choice:int = 0) -> str:
    red = lambda s: colored(s, color='red')
    yellow = lambda s: colored(s, color='yellow', attrs=['bold'])
    magenta = lambda s: colored(s, color='magenta', attrs=['bold'])
    cyan = lambda s: colored(s, color='cyan')
    def colorize(current_choice:int) -> callable:
        if current_choice == prize and prize & visibility == prize:
            return magenta
        elif (not user_choice & visibility or visibility == 7) and current_choice == user_choice:
            return yellow
        elif current_choice & visibility and (not prize & visibility or visibility == 7):
            return red
        else:
            return cyan

    def getLines(words:list, expression:str, number:int) -> str:
        res = str()
        alnl = lambda length, i: '\n' if i == length-1 else ''

        for current_choice, word in zip(bits, words):
            exp_glob = {"word":word}
            if number:
                exp_glob['length'] = len(word) + number
            res += colorize(current_choice)(eval(f"f\"{expression}\"", exp_glob)) + alnl(3, to_int(current_choice) - 1)
        return res

    values = {"visible": ["GOAT", "CAR"], "hidden": "DOOR"}
    strValues = [values["hidden"] if not cb & visibility else values["visible"][cb == prize] for cb in bits]
    expressions = ["{'-'*length}\t", "|{' '*length}|\t", "|  {word}{' '*2}|\t", "|{' '*length}|\t", "{'-'*length}\t"]
    exp_nums = [6, 4, 0, 4, 6]
    res = str()

    for exp, num in zip(expressions, exp_nums):
        res += getLines(strValues, exp, num)

    return res

def generate():
    return choice(bits)

def new_choice(prize:int, visibility:int, user_choice:int) -> int:
    choice = 7 - (visibility | user_choice)
    append(display(prize, visibility, choice), res=True)
    append(f"You decided to change choosing the door n. {to_int(choice)}")
    return choice

def open_door(prize:int, user_choice:int):
    if prize & user_choice:
        return choice(tuple(set(bits) - {user_choice}))
    else:
        return 7 - prize - user_choice

def choose(prompt:str, values:tuple) -> str:
    values = [str(value) for value in values]
    def process_values(values:tuple) -> str:
        if len(values) == 1:
            return values[0]
        res = str()
        for i, value in enumerate(values):
            res += value
            if i < len(values) - 2:
                res += ', '
            elif i == len(values) - 2:
                res += ' and '
        return res

    while True:
        out_print()
        if (this_choice := input(prompt + '\n> ')) in values:
            break
        else:
            print(f"You must choose between {process_values(values)}.\n{this_choice} is not a valid choice! Please, try again. (press enter)")
            input()
    return this_choice

def points():
    for i in range(3):
        sleep(1)
        append('.', end='')
        out_print()
    sleep(1)
    append()

if __name__ == '__main__':
    try:
        while True:
            prize       = generate()
            visibility  = 0

            append(display(), res=True)
            append("\nBehind these doors there one brand new car and two goats.")

            user_choice = to_bin(int(choose("Try and win the car choosing the right door typing 1, 2 or 3!", (1,2,3))))
            append(display(prize, visibility, user_choice), res=True)
            opened_door = open_door(prize, user_choice)
            visibility |= opened_door

            append(f"You choose the door n. {to_int(user_choice)}")
            out_print(1)
            append(f"\nNow I will open the door n.{to_int(opened_door)}", end='')
            points()
            append(display(prize, visibility, user_choice), res=True)
            out_print(2)

            if choose("Would you like to change your previous choice? (y/n): ", ('y','n')) == 'y':
                user_choice = new_choice(prize, visibility, user_choice)

            visibility = 7
            out_print(1)
            append("Now I will open all the doors", end='')
            points()
            append(display(prize, visibility, user_choice), res=True)
            append("YOU WON!" if prize & user_choice else "YOU LOST...")
            out_print()
            if choose("Would you like to play again? (y/n)", ('y','n')) == 'n':
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        print("\n\nExecution terminated\n")
