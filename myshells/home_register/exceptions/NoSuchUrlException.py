class NoSuchUrlException(Exception):
    def __init__(self, url):
        self.url = url
        # super().__init__(f"There's no {self.url} in scrapers")

    def __str__(self):
        return repr(f"There's no {self.url} in scrapers")

