from sys import argv, exit
from time import sleep, localtime, ctime
from os import *
from pynput.keyboard import Key, Controller
from getpass import getpass
from threading import Thread

if len(argv) > 1:
    if argv[1] == '--edit':
        system(f"atom {argv[0]}")
        exit(0)
    elif argv[1] == '--del':
        system(f"rm -fri /Users/mr.anderson2159/Documents/diary")
        exit(0)

diary_path = argv[1] if len(argv) == 2 else "/Users/mr.anderson2159/Documents/diary.zip"
diary_basename = ''
zip_basename = ''
unzip_diary_folder = ''
del_thread = None
keyboard = Controller()
password = ''

def set_cwdir():
    global diary_basename, zip_basename, unzip_diary_folder
    dir_path = path.dirname(diary_path)
    if path.splitext(diary_path)[1] != '.zip':
        raise Exception("Path must be of a zip file")
    if dir_path:
        chdir(dir_path)
    zip_basename = '"' + path.basename(diary_path) + '"'
    diary_basename = zip_basename[:-5] + '"'
    unzip_diary_folder = listdir('.')

def enter_password(faster: bool = False):
    for char in password:
        keyboard.press(char)
        keyboard.release(char)
        if not faster:
            sleep(.1)
    if not faster:
        sleep(.3)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

class Pass_thread(Thread):
    def __init__(self, time: int, faster: bool = False):
        Thread.__init__(self)
        self.time = time
        self.faster = faster

    def run(self):
        sleep(self.time)
        enter_password(self.faster)

class Delete_thread(Thread):
    def run(self):
        global unzip_diary_folder
        while len(unzip_diary_folder) == len(listdir('.')):
            sleep(.2)
        unzip_diary_folder = '"' + [file for file in listdir('.') if file not in unzip_diary_folder][0] + '"'
        system(f"open {diary_basename}")

def unlock_diary():
    global password, del_thread
    print(f"opening {diary_path}\n")
    password = getpass()
    system(f"open {zip_basename}")
    sleep(1)
    enter_password()
    del_thread = Delete_thread()
    del_thread.start()

def process_date():
    l = localtime()
    y = l.tm_year
    m = l.tm_mon
    d = l.tm_mday
    wd = l.tm_wday
    g = ["lunedì", "martedi", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
    g = list(map(lambda s : s[0].upper() + s[1:], g)) # per pigrizia, sia chiaro
    return f"{g[wd]}\\ {d}\\:{m}\\:{y}"


def open_today_page():
    date = process_date()
    del_thread.join()
    file_path = f"{unzip_diary_folder}/{date}.txt"
    is_new = False
    if not path.exists(file_path):
        system(f"touch {file_path}")
        is_new = True
    t = '"' + ('\n\n\n' if is_new else '') + ctime().split(' ')[3] + '\n"'
    system(f"echo {t} >> {file_path} && open {file_path}")


def wait_for_closing():
    while True:
        if input("Done? (y/n): ").lower() == "y":
            break
    Pass_thread(.5, True).start()
    Pass_thread(1, True).start()
    system(f"zip -er {unzip_diary_folder} {unzip_diary_folder} && rm -fr {unzip_diary_folder}")

system("clear")
print("Diary v1.0\n")

try:
    set_cwdir()
    unlock_diary()
    open_today_page()
    wait_for_closing()
    sleep(2)
    system("clear")
except:
    print("\n\n\x1b[31mApplication closed\n\x1b[0m")
