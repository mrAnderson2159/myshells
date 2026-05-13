from exceptions.NoSuchUrlException import NoSuchUrlException
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from src.session import Session
from requests.exceptions import *

class Scrape():
    def __init__(self, session: Session):
        self.session = session
        self.__scrapers = {
            "www.ebay.it": self.ebay
        }

    def switch(self, urls):
        domain, url = self.find(urls)
        try:
            return self.__scrapers[domain](self.session.get(url))
        except KeyError:
            raise NoSuchUrlException(domain)
        except HTTPError:
            return self.switch([u for u in urls if u != url])
        except AttributeError as e:
            return self.switch([u for u in urls if u != url])
            #raise Exception(e.__str__(), url)

    def ebay(self, html:BeautifulSoup):
        name = html.find(id='itemTitle')
        span = name.span.text
        name = name.text.replace(span, '').strip()
        image = html.find(id='icImg')["src"]
        return name, image

    def find(self, urls):
        is_first = True
        first = None
        sites = self.__scrapers.keys()
        for url in urls:
            domain = urlparse(url).netloc
            print(url)
            if is_first:
                first = domain, url
                is_first = False
            if domain in sites:
                return domain, url
        return first