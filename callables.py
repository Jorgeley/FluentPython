import random


class Bingo:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    # overwriting to make the class callable
    def __call__(self):
        return self.pick()


# a callable instance
bingo = Bingo(range(100))
print(bingo())
print(bingo())
