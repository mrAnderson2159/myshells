import speech_recognition as sr

class Recognizer:
    @classmethod
    def listen(cls, phrase_time_limit = None):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=phrase_time_limit)
            try:
                return r.recognize_google(audio, language="it-IT");
            except Exception as e:
                return None
