from src.session  import Session
from src.specific import Scrape
from googlesearch import search, lucky
from threading import Thread
from urllib.parse import urlparse
import json

games = {}

class MyThread(Thread):
    def __init__(self, barcode):
        Thread.__init__(self)
        self.barcode = barcode

    def run(self) -> None:
        Session.do(scrape, barcode=barcode)

class WriteThread(Thread):
    def __init__(self, barcode, results):
        Thread.__init__(self)
        self.barcode = barcode
        self.results = results

    def run(self) -> None:
        urls = search(self.barcode, tld="com", stop=20, pause=2.0)
        if not self.barcode in self.results:
            self.results[self.barcode] = []
            for url in urls:
                url = urlparse(url).netloc
                if not url in self.results[self.barcode]:
                    self.results[self.barcode].append(url)


def collect():
    threads = []
    with open("db.json") as db:
        results = json.load(db)

    while True:
        barcode = input("inserisci il codice a barre: ")
        if barcode == 'stop':
            for thread in threads:
                thread.join()
            write(results)
            break
        t = WriteThread(barcode, results)
        threads.append(t)
        t.start()

def scrape(session, barcode):
    scrape = Scrape(session)
    urls = search(barcode, tld="com", stop=20)
    name, image = scrape.switch(urls)
    games[name] = image

def write(obj):
    with open("db.json", 'w') as db:
        db.write(json.dumps(obj))

if __name__ == '__main__':

    # barcode = '5035224112876'
    # Session.do(scrape, barcode=barcode)
    # threads = []
    # while True:
    #     barcode = input("inserisci il codice a barre: ")
    #     if barcode == 'stop':
    #         for thread in threads:
    #             thread.join()
    #         print(games)
    #         break
    #     #Session.do(scrape, barcode=barcode)
    #     t = MyThread(barcode)
    #     threads.append(t)
    #     t.start()

    collect()