from bs4 import BeautifulSoup as bs
import requests

class Session:
        def __init__(self, session):
            self.session = session

        def get(self, url, **kwargs):
            return self.__request(url, self.session.get, kwargs)

        def post(self, url, **kwargs):
            return self.__request(url, self.session.post, kwargs)

        def __request(self, url, method, kwargs):
            answer = method(url, **kwargs) #?
            answer.raise_for_status()
            return bs(answer.content, features="html.parser")

        @staticmethod
        def do(callback: callable, **kwargs):
            with requests.Session() as s:
                s = Session(s)
                return callback(s, **kwargs)
