from inspect import getgeneratorstate
"""
COROUTINES (Consumers of Data)
A coroutine is syntactically like a generator: just a function with the yield keyword in its body.
However, in a coroutine, yield usually appears on the right side of an expression (e.g., datum = yield),
and it may or may not produce a value if there is no expression after the yield keyword,
the generator yields None. The coroutine may receive data from the caller, which uses .send(datum)
instead of next(...) to feed the coroutine. Usually, the caller pushes values into the coroutine.
IN SIMPLE WORDS: a coroutine is a generator that yields expressions sent by the client code.
Coroutines are perfect for concurrent tasks.
"""


def simple_coroutine():  #
    print('-> coroutine started')
    """
    notice that the 'yield' is on the right side, 
    usually a generator would do 'yield x', that's
    the syntax difference of coroutine and generator
    """
    x = yield  # remember that we have to read right to left, so yield happens first which stops execution
    print('-> coroutine received:', x)


my_coro = simple_coroutine()
print(my_coro)
next(my_coro)  # this starts the coroutine and stops at yield, 'x' isn't assigned
try:
    my_coro.send(42)  # send 42 as x to the coroutine
except StopIteration:
    my_coro.close()


# getting the status of the coroutine:
def simple_coro2(a):
    print('-> Started: a =', a)
    """
    remember that expression is evaluated before assignment (right to left), so
    the execution stops at 'yield a' and b only is assigned in the next iteration
    """
    b = yield a
    print('-> Received: b =', b, ', previous a = ', a)
    """
    we're returning/yielding 'a + b' to the client code and at the same time stopping execution
    until next iteration when 'c' will be assigned and code execution carry on
    """
    c = yield a + b
    print('-> Received: c =', c, ', previous a = ', a, ', previous b = ', b)


my_coro2 = simple_coro2(14)
print(getgeneratorstate(my_coro2))
# 14 is assigned to 'a' and code execution stops at 'yield a', 'b' isn't assigned, 14 is returned as result of 'yield a'
yielded = next(my_coro2)
print('yielded = ', yielded)
print(getgeneratorstate(my_coro2))
# 28 is assigned to 'b' and code execution stops at 'yield a + b', 'c' isn't assigned,
# 42 is returned as result of 'yield a + b'
yielded = my_coro2.send(28)
print('yielded = ', yielded)
print(getgeneratorstate(my_coro2))
try:
    # 99 is assigned to 'c' and code execution finishes
    my_coro2.send(99)
except StopIteration:
    my_coro2.close()
print(getgeneratorstate(my_coro2))


# an useful example:
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        try:
            term = yield average
            total += term
            count += 1
            average = total/count
        except Exception:
            pass

averager = averager()
print(next(averager))
print(averager.send(100))
print(averager.send(500))
print(averager.send(50))
print(averager.send('x'))
print(averager.send(350))
print(averager.send('x'))
averager.close()


"""
This is the convention for coroutines:
    [     CALLER    ]---send---[ DELEGATING]-------->[     SUB    ]
    [ (client code) ]<---------[ GENERATOR ]--yield--[  GENERATOR ]
"""
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# the sub generator
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


# the delegating generator, it works like a tunnel between the client code and the sub generator
def grouper(_results, key):
    while True:
        _results[key] = yield from averager()


# the client code, a.k.a. the caller
data = {
    'girls;kg': [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m': [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg': [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m': [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
results = {}
for key, values in data.items():
    group = grouper(results, key)  # creating a coroutine 'delegating generator' for every group
    next(group)  # priming the coroutine
    for value in values:  # send values one by one to the group coroutine primed previously
        group.send(value)
    group.send(None)  # important! to finish the coroutine and free the 'delegating generator' coroutine
print(results)
