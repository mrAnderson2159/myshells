import sys
from os import system, path
from os.path import exists
from src.operation import Operation
from src.functions import video_audio_converter
from src.cloud_loader import upload
from src.transcriptor import transcriptor
sys.path.append(path.expanduser("~/myshells/pyplugs"))
from switch import Switch
from typing import *
from debug import debug
from utils import indent_lines, get_parent_dir
from pyerrors import *

def edit() -> None:
    os.system(f"open -a 'PyCharm CE' '{get_parent_dir(__file__)}'")

def usage(indentation:int = 0) -> str:
    usage = '\n'
    usage += 'sbobinatore [PERCORSO_VIDEO, CARTELLA_DI_DESTINAZIONE]'
    usage += '\n'
    return indent_lines(usage, indentation)

def UnknownFlagError(flag:str) -> None:
    raise F01(flag + usage(1))

def default(video: str, output: str):
    if not exists(video):
        raise FileNotFoundError(f"Il file {video} non esiste")

    system('clear')

    o = Operation('Avvio il programma').start()
    print()

    audio = video_audio_converter(video, output)
    gs = upload(audio, 'lezioni-sbobinatore')
    transcription, output, override = transcriptor(gs, video)

    if override:
        with open(output, 'w') as file:
            file.write(transcription)

    print('\n\nTempo totale: ', end='')
    o.stop()

def main(argv: List[str]) -> None:
    try:
        with Switch(argv[1]) as s:
            s.exit_case('--edit', edit)
            s.default(default, argv[1], argv[2])
    except IndexError:
        raise F00(usage(1))

if __name__ == '__main__':
    main(sys.argv)