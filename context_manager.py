import contextlib


class LookingGlass:
    # this is executed once in the 'with' start
    def __enter__(self):
        import sys

        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return "CONTEXT MANAGER"

    def reverse_write(self, text):
        self.original_write(text[::-1])

    # this is executed once when exiting the 'with' block
    def __exit__(self, exc_type, exc_value, traceback):
        import sys

        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please DO NOT divide by zero!")
            # returning True to tell the compiler that exception was handled,
            # otherwise, it will propagate
            return True


with LookingGlass() as lg:
    print("reversed string")
    1 / 0  # this will be be caught by the if block in the exit method
print("normal string")
print(lg)


# another way of doing the same thing:
@contextlib.contextmanager
def looking_glass():

    # replaces the enter() method
    import sys

    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    # executed before the while block
    sys.stdout.write = reverse_write
    yield "CONTEXT MANAGER 2"
    # executed after the while block
    sys.stdout.write = original_write


with looking_glass() as lg:
    print("reversed string 2")
print("normal string 2")
print(lg)
