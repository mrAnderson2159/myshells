class Fiend:
    def __init__(self, name: str, captured: int = 0):
        self.name = ' '.join(map(str.capitalize, name.split(' ')))
        self.captured = captured

    def __add__(self, number: int) -> 'Fiend':
        if self.captured < 10:
            self.captured = min(10, self.captured + number)
        return self

    def __sub__(self, number: int) -> 'Fiend':
        if self.captured > 0:
            self.captured = max(0, self.captured - number)
        return self

    def __str__(self):
        return f'{self.name}{{ {self.captured} }}'

    def __repr__(self):
        return str(self)

    def get_captured(self):
        return self.captured

    def get_name(self):
        return self.name
