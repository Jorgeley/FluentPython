import functools
import html
import numbers
import time
from collections import abc

from designpatterns.strategy import pedidoZe

"""
A decorator is a callable that takes another function as argument
(the decorated function).
The decorator may perform some processing with the decorated function, and
returns it or replaces it with another function or callable object.
"""


def decorator1(func):
    return lambda: print("decorator1")


@decorator1
def target1():
    print("target 1")  # this will be replaced since decorator1 return differs


target1()


def decorator2(func):
    print("decorator2")
    return func


@decorator2
def target2():
    print(
        "target2"
    )  # now that decorator2 returns decorated function, both codes execute


target2()


# usability
def pow2(summed):
    return summed() ** 2


@pow2
def sum():
    return 2 + 4


print(sum)

"""
important to understand the order of execution
"""
registry = []


def register(func):
    print("running register(%s)" % func)
    registry.append(func)
    return func


@register
def f1():
    print("running f1()")


@register
def f2():
    print("running f2()")


def f3():
    print("running f3()")


def main():
    print("running main()")
    print("registry ->", registry)
    f1()
    f2()
    f3()


main()


# a good example:
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        print("[%0.8fs] %s(%s) -> %r" % (elapsed, name, arg_str, result))
        return result

    return clocked


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


factorial(5)


"""
built-in decorators: python comes with some useful standard
decorators like @functools.*
look at this memoization technique for a fibonacci function:
"""


@clock
def fibonacci_not_memoized(n):
    if n < 2:
        return n
    return fibonacci_not_memoized(n - 2) + fibonacci_not_memoized(n - 1)


print("running fibonacci not memoized")
print(fibonacci_not_memoized(9))


@clock
@functools.lru_cache()
def fibonacci_memoized(n):
    if n < 2:
        return n
    return fibonacci_memoized(n - 2) + fibonacci_memoized(n - 1)


print("running fibonacci memoized")
print(fibonacci_memoized(9))


"""
Another good built-in decorator is @singledispatch, it makes a function as ge-
neric, it can be called in different manners, like a overloaded method in OOP
"""


# this is the base function which will be generalized
@functools.singledispatch
def htmlize(obj):
    print("htmlize default version")
    content = html.escape(repr(obj))
    return "<pre>{}</pre>".format(content)


# this is one of the versions of the base function
@htmlize.register(str)
def _(
    text,
):  # the name of the function is irrelevant and it's a good practice to make
    # this clear
    print("htmlize str version")
    content = html.escape(text).replace("\n", "<br>\n")
    return "<p>{0}</p>".format(content)


# another version
@htmlize.register(numbers.Integral)
def _(n):
    print("htmlize int version")
    return "<pre>{0} (0x{0:x})</pre>".format(n)


#  another 2 versions
@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    print("htmlize tuple version")
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>"


print(htmlize("this is a string"))
print(htmlize(999.99))
print(htmlize([1, "x", 5.55, True]))
print(htmlize({"x", 8.88}))


"""
Decorators with parameters: you can have a function with parameters to be
used by an inner function (the actual decorator), like a decorator factory
"""
registry = set()


def register(active=True):  # this is the decorator factory
    def decorate(func):  # this is the actual decorator
        print("running register(active=%s)->decorate(%s)" % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func  # returning the decorated function

    return decorate  # returning the decorator since register() is the factory
    # of decorators


@register(active=False)
def _f1():
    print("running f1()")


@register()
def _f2():
    print("running f2()")


"""
real scenario example:
"""
promos = []


def promotion(promo_func):
    promos.append(promo_func)
    return promo_func


@promotion
def fidelity(order):
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


@promotion
def bulk_item(order):
    """10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount


@promotion
def large_order(order):
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07
    return 0


def best_promo(order):
    """Select best discount available"""
    print(promos)
    return max(promo(order) for promo in promos)


print(best_promo(pedidoZe))


# decorators in classes:
def do_something_else(f):
    def wrapper(*args, **kwargs):
        instance = args[0]  # the 1st argument is always instance of the class
        print(
            "doing something else with args or kwargs",
            instance,
            args,
            kwargs
        )
        return f(*args)

    return wrapper


class Task(object):
    @do_something_else
    def do_something(self, task: str = ""):
        print("doing something " + task)


Task().do_something("my task")
