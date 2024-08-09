import json

class JSON_database:
    def __init__(self, path: str):
        self.__path = path
        with open(path, 'r') as db_file:
            self.database = json.load(db_file.read())

    def __repr__(self):
        return self.database

    def post(self):
        with open(path, 'w')  as db_file:
            db_file.write(json.dumps(self.database))

    def p(self):
        print(self.database)

    @property
    def path(self):
        return self.path
