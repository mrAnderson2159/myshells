import sys
from os import system
from os.path import exists
from src.operation import Operation
from src.functions import video_audio_converter
from src.cloud_loader import upload
from src.transcriptor import transcriptor

if len(sys.argv) < 3:
    raise ValueError(
        "utilizzo: sbobinatore [PERCORSO_VIDEO, CARTELLA_DI_DESTINAZIONE]"
    )

video, output = sys.argv[1:3]

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

print('Tempo totale: ', end='')
o.stop()

