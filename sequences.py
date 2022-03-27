"""
some cool stuff we can do with sequences
"""

l = [('x',) * 3] # a list within a tuple within 3 'x'
print(l)

l = ('*',) * 3 # a tuple within 3 '*'
print(l)

# a tictactoe board
tictactoe = [['_'] * 3 for i in range(3)]
print(tictactoe)

# easily unpack a tuple
packed = ('unpack', 'this')
print('%s %s' % packed)
# or even better:
print("%s " * packed.__len__() % packed)

l = ['x', 'y', 'z']
l *= 3 # extending 3 times the list items
print(l)

# combining collections
from collections import ChainMap
chainmap = ChainMap({"a":1, "b":2}, {"c":3, "d":4}, {"e":5, "f":6})
print(chainmap)
print(chainmap.get("e"))
d = { **{"a":1, "b":2}, **{"a":11, "b":22, "c": 3} }
print(d)

# ranking
from collections import Counter
c = Counter(["a", "b", "c", "a", "b", "c", "c", "c", "d"])
print(c.most_common(1)) # [('c', 4)]
print(c.most_common()[-1]) # ('d', 1)

# sets (they are immutables)
search = {2, "a", "z", "b", 9}
list_ = {1, 3, 5, "a", "b", "c", "d"}
found = search & list_
print("found", found)
# sets are useful for removing duplicates
duplicateds = ["z", "a", "b", "b", "a", 1, "a", 1, "z", 9]
uniques = set(duplicateds)
print(uniques)
# diff of 1st set to 2nd one:
diff = {'t', 'x', 'y', 'z', 'q'} - {'y', 'x', 'w', 'z'}
print(diff)

# this is a good library for computing time
from time import perf_counter as pc
from random import random
from array import array

# 10 million list numbers, costs around 15s
t0 = pc(); floats2 = list((random() for i in range(10**7))); print(pc() - t0)
# same with tuple
t00 = pc(); floats22 = tuple((random() for i in range(10**7))); print(pc() - t00)
# but array is faster!
t000 = pc(); floats222 = array('d', (random() for i in range(10**7))); print(pc() - t000)

# benchmark dict X set (Macbook Pro 2.6 GHz 6-Core Intel Core i7, 16 GB 2667 MHz DDR4)
def dict_benchmark():
    haystack = dict.fromkeys((random() for i in range(10 ** 3)))
    needles = {"a":3}
    found = 0
    for n in needles:
        if n in haystack: found += 1
def set_benchmark():
    haystack = {(random() for i in range(10 ** 3))}
    needles = {"a"}
    found = haystack & needles
from timeit import timeit
timeit(lambda: dict_benchmark()) # around 167ms
timeit(lambda: set_benchmark()) # around 0.87ms
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