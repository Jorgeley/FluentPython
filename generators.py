import itertools

"""
Generators are functions that yields values rather than return,
the difference is that while functions execute the whole body until the return,
generators, in the other hand stop in the yield keyword and only executes the
rest of the code in subsequent calls. Generators are iterators. Generators save memory!
"""


def simple_generator():
    print('start generator')
    yield 2
    print('continue generator')
    yield 5
    print('stop generator')
    yield 9


# generators have to be iterated
g = simple_generator()
print(g)
next(g)
next(g)
next(g)
# next(g)  # this will trigger StopIteration exception
print([g * 2 for g in simple_generator()])  # we can iterate the whole generator, of course

# itertools have some built-in useful generators
gen = itertools.count(1, .5)
print(type(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))

# this is called a "generator expression"
g = (g for g in [2, 5, 7])
print(g)


# you can 'yield from' any iterator:
def string_generator(s: str) -> str:
    yield from s
    """
    'yield from s' is the same as (supposing s = 'xyzw'):
        def _():
            yield 'x'
            yield 'y'
            yield 'z'
            yield 'w'
    if few words, we're yielding the yielded iterator, like 2 nested generators
    """


for s in string_generator('xyzw'):
    print(s, "- yielded from 'xyzw'")


# this is interesting:

# WRONG: nested loops, works but ugly code
def wrong_nested_loops_generator(*iterables):
    for it in iterables:
        for i in it:
            yield i


print(list(wrong_nested_loops_generator('XYZ', [10, 30, 500])))


# CORRECT: yielding the yielded (chained generator), much more readable
def correct_yielding_yielded_generator(*iterables):
    for i in iterables:
        yield from i  # "yielding the yielded 'i'"


print(list(correct_yielding_yielded_generator('WQA', [100, 300, 50])))


# EVEN BETTER:
def gen():
    yield from 'AB'  # same as `for c in 'AB' yield c`
    yield from range(1, 3)  # same as `for i in range(1, 3) yield i`


print(list(gen()))


# to understand better the "yield from", but don't do this, just for better understanding
def f():
    def do_yield(n):
        yield n

    x = 0
    while True:
        x += 1
        yield from do_yield(x)  # yielding the yielded "do_yield(n)"


ff = f()
print(next(ff))
print(next(ff))
print(next(ff))
