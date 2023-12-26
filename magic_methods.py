# they are useful builtin methods we can overload/override

import time


# of course, the simplest ones
class Basic:
    # constructor
    def __init__(self):
        # executed on class instantiation
        print("instantiating", self)

    # deconstruct (don't confuse with __delete__)
    def __del__(self):
        # executed on garbage collection, deconstruction
        print("I'm deleted now :(", self)


a = Basic()
time.sleep(2)  # just to give some delay so we can see both methods called in
# their correct scope


# we can leverage objects operations like addition, subtraction
class Result:
    # supposing a class where results will be accumulated
    def __init__(self, result: float):
        self.result = result

    # here's the magic: returning a new instance with attributes summed
    def __add__(self, other):
        return Result(self.result + other.result)

    # same thing for subtraction
    def __sub__(self, other):
        return Result(self.result - other.result)


result1 = Result(33)
result2 = Result(44)
combined_result = result1 + result2
print(combined_result.result)
result3 = Result(55)
combined_result = combined_result - result3
print(combined_result.result)


class ObjectRepresentation:
    """
    useful methods for printing objects, if none of these methods are
    implemented, print will return something like
    <class '__main__.ObjectRepresentation'>
    """

    def __init__(self, name: str):
        self.name = name

    # 'representation' of an object, useful for debugging purposes
    def __repr__(self):
        print(f"name: {self.name}, type: {type(self)}")

    """
    this is more user friendly representation, IT CALLS __repr__
    IF NOT IMPLEMENTED to see the difference, comment out this method and
    you'll see that __repr__ is called
    """

    def __str__(self):
        return f"name: {self.name}"


object_representation = ObjectRepresentation("Jojo")
print(object_representation)
