from os import system


class Printer:
    def print_out(self, text: str, cpi: int = 6, lpi: int = 3, page_left: int = 36):
        system(f'echo "{text}" | lp -o cpi={cpi} -o lpi={lpi} -o page-left={page_left}')
