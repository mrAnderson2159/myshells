from subprocess import Popen
from datetime import timedelta
from google.cloud import speech
from src.operation import Operation
from src.functions import timedelta_truncation
from typing import Tuple
from os.path import exists
from utils import confirm
from os.path import splitext


def transcriptor(uri: str, output: str, language: str = 'it_IT') -> Tuple[str, str, bool]:
    text = ''
    output = splitext(output)[0] + '.txt'
    if not exists(output) or confirm(
        f"la trascrizione {output} esiste già, desideri sovrascriverla"
    ):
        o = Operation("Creo speech client").start()
        speech_client = speech.SpeechClient()
        o.stop().new("Creo long audio e configurazione").start()
        long_audio = speech.RecognitionAudio(uri=uri)
        config = speech.RecognitionConfig(
            enable_automatic_punctuation=True,
            language_code=language,
            use_enhanced=True,
            sample_rate_hertz=44100,
            audio_channel_count=2
        )
        o.stop().new("Inizio lettura").start()
        operation = speech_client.long_running_recognize(
            config=config,
            audio=long_audio
        )
        o.stop().new("Inizio trascrizione").start()
        p = Popen(['python3', "/Volumes/working space/myshells/keep-alive.py"])
        response = operation.result(timeout=3600)
        p.kill()
        o.stop().new("Scrivo chuck").start()

        t = timedelta(seconds=0)
        for i, result in enumerate(response.results):
            print(f'\rScrivo chunk {i + 1}', end='')
            text += str(t) + '\n'
            text += result.alternatives[0].transcript.strip() + '\n\n'
            t = timedelta_truncation(result.result_end_time)
        return text, output, True
    else:
        with open(output, 'r') as file:
            text = file.read()
        return text, output, False
