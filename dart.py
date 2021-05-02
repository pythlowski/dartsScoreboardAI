import re


class Dart:
    def __init__(self, *args):
        if type(args[0]) == str:
            self.dart_from_string(args[0])
        else:
            self.dart_from_values(*args)

    def dart_from_values(self, sector: int, multiplier: int):
        self.sector = sector
        self.multiplier = multiplier

    def dart_from_string(self, dart_string: str):
        dart_string = dart_string.upper()
        if dart_string == 'BULL' or dart_string == '50':
            self.sector, self.multiplier = 25, 2
        elif dart_string == 'OUT':
            self.sector, self.multiplier = 0, 1
        else:
            self.sector = int(re.search("\d+", dart_string).group(0))
            assert self.sector in [*range(0, 21), 25]
            self.multiplier = {'D': 2, 'T': 3}.get(dart_string[0], 1)

    def score(self):
        return self.sector * self.multiplier

    def __str__(self):
        if self.sector == 25 and self.multiplier == 2:
            return 'BULL'
        elif self.sector == 0:
            return 'OUT'
        elif self.multiplier == 1:
            return str(self.sector)
        elif self.multiplier == 2:
            return f'D{self.sector}'
        elif self.multiplier == 3:
            return f'T{self.sector}'


if __name__ == '__main__':
    print(str(Dart("x20")))
