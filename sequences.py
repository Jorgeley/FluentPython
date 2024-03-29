from array import array
from collections import ChainMap, Counter
from random import random
# this is a good library for computing time
from time import perf_counter as pc
from timeit import timeit

"""
some cool stuff we can do with sequences
"""

_list = [("x",) * 3]  # a list within a tuple within 3 'x'
print(_list)

_list = ("*",) * 3  # a tuple within 3 '*'
print(_list)

# a tictactoe board
tictactoe = [["_"] * 3 for i in range(3)]
print(tictactoe)

# easily unpack a tuple
packed = ("unpack", "this")
print("%s %s" % packed)
# or even better:
print("%s " * packed.__len__() % packed)

_list = ["x", "y", "z"]
_list *= 3  # extending 3 times the list items
print(_list)

# combining collections
chainmap = ChainMap({"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6})
print(chainmap)
print(chainmap.get("e"))
d = {**{"a": 1, "b": 2}, **{"a": 11, "b": 22, "c": 3}}
print(d)

# ranking
c = Counter(["a", "b", "c", "a", "b", "c", "c", "c", "d"])
print(c.most_common(1))  # [('c', 4)]
print(c.most_common()[-1])  # ('d', 1)

# sets (they are immutables)
search = {2, "a", "z", "b", 9}
list_ = {1, 3, 5, "a", "b", "c", "d"}
found = search & list_
print("found", found)
# sets are useful for removing duplicates
duplicateds = ["z", "a", "b", "b", "a", 1, "a", 1, "z", 9]
uniques = set(duplicateds)
print(uniques)
s1 = {"t", "x", "y", "z", "q"}
s2 = {"y", "x", "w", "z"}
# diff of 1st set to 2nd one:
diff = s1 - s2
print(diff)
# union
united_set = s1 | s2
print(united_set)

# combining multiple lists into a tuple of lists
uuids = ["uuid1", "uuid2", "uuid3", "uuid4"]
emails = [
    "someone1@mail.com",
    "someone2@mail.com",
    "someone3@mail.com",
    "someone4@mail.com",
]
addresses = [
    "1, Main St. - New York",
    "9, Downtown - Los Angeles",
    "3, Paulista Ave. - Sao Paulo",
    "2, Dammit Ave. - Boston",
]
records = zip(uuids, emails, addresses)
for r in records:
    print("records zipped from lists", r)
# we can also do the opposite, unzip it
records = zip(uuids, emails, addresses)
_uuids, _emails, _addresses = zip(*records)
print("_uuids", _uuids)
print("_emails", _emails)
print("_addresses", _addresses)


# 10 million list numbers, costs around 15s
t0 = pc()
floats2 = list((random() for i in range(10 ** 7)))
print(pc() - t0)
# same with tuple
t00 = pc()
floats22 = tuple((random() for i in range(10 ** 7)))
print(pc() - t00)
# but array is faster!
t000 = pc()
floats222 = array("d", (random() for i in range(10 ** 7)))
print(pc() - t000)


# benchmark dict X set
# (Macbook Pro 2.6 GHz 6-Core Intel Core i7, 16 GB 2667 MHz DDR4)
def dict_benchmark():
    haystack = dict.fromkeys((random() for i in range(10 ** 3)))
    needles = {"a": 3}
    found = 0
    for n in needles:
        if n in haystack:
            found += 1


def set_benchmark():
    haystack = {(random() for i in range(10 ** 3))}
    needles = {"a"}
    _found = haystack & needles
    print(_found)


timeit(lambda: dict_benchmark())  # around 167ms
timeit(lambda: set_benchmark())  # around 0.87ms
# you can also test from command line:
"""
python3 -m timeit '
from random import random
haystack = dict.fromkeys((random() for i in range(10 ** 3)))
needles = {"a":3}
found = 0
for n in needles:
    if n in haystack: found += 1
'
"""
"""
python3 -m timeit '
haystack = {(random() for i in range(10 ** 3))}
needles = {"a"}
found = haystack & needles
'
"""
