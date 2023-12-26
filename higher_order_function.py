"""
A function is called Higher Order Function (HOF) if it contains other
functions as a parameter or returns a function as an output.
Closure is the technique used to make the variable accessible by the nested
function, in the example bellow, 'series' is that variable
"""


def make_averager_hof():

    # init of closure
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    # end of closure

    return averager


avg = make_averager_hof()
print(avg(10))
print(avg(20))
print(avg(60))

# we can inspect the scopes
print(avg.__code__.co_varnames)
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
