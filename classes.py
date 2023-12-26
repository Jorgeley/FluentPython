# basic inheritance
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass


class Parent:
    def output(self, message):
        print(f"output message '{message}' from {Parent}")

    def output2(self, message):
        print(f"output2 another message '{message}' from {Parent}")

    def output3(self, message):
        print(f"output3 message '{message}' from {Parent}")


class Child(Parent):

    # overload
    def output(self, message):
        print(f"output '{message}' from {self.__class__}")
        super(Child, self).output(message)

    # @override
    def output2(self, message):
        print(f"output2 '{message}' from {self.__class__}")


child = Child()
child.output("testing inheritance")
child.output2("testing inheritance")
child.output3("testing inheritance")


# multiple inheritance


class JamieLannister:
    def output(self):
        print("Jofrey, I'm your father")


class CerseyLannister:
    def output(self):
        print("Jofrey, I'm your mother")


# JamieLannister and CerseyLannister are inherited by Jofrey, hence they
# are siblings
class Jofrey(JamieLannister, CerseyLannister):
    def output(self):
        super().output()

    def output2(self):
        """
        MRO (method resolution order): Jofrey->JamieLannister->CerseyLannister
        passing the 1st argument, tells super to get the next in the MRO, in
        this case CerseyLannister
        """
        super(JamieLannister, self).output()


jofrey = Jofrey()
print(f"this is the inheritance order: {Jofrey.__mro__}")
jofrey.output()
jofrey.output2()


# abstract class, they can't be instantiated, it works like an interface


class AbstractPainter(ABC):
    @abstractmethod
    def paint(self):
        print("painting")


class ConcretePainter(AbstractPainter):
    # won't work, we have to override the parent methods
    pass


class ConcretePainter2(AbstractPainter):
    def paint(self):
        super().paint()


# abstractPainter = AbstractPainter()  # TypeError: Can't instantiate abstract
# class AbstractPainter
# AbstractPainter.paint()  # also won't work, since the method is supposed to
# be used in a child class
# concretePainter = ConcretePainter()  # won't work either because we didn't
# override the paint method
concretePainter = ConcretePainter2()
concretePainter.paint()


# classmethod decorator makes a class be referenced directly, not only by
# its instance
class MyClass:
    @classmethod
    def output(cls):
        print("classmethod")


myClass = MyClass()
myClass.output()
MyClass.output()  # this is only possible by the @classmethod decorator


# composition


class Weapon:  # the component class
    _name: str
    _damage: int

    # leveraging the constructor special/magic method
    def __init__(self, name: str, damage: int = 10) -> None:
        self._name = name
        self._damage = damage

    def hit(self):
        print("Attack! Attack! Attack! ")
        print(f"\t\t*damage caused: {self._damage}")


class Warrior:  # the composite class
    _name: str
    _weapon: Weapon  # this is the composition relation

    def __init__(self, name: str, weapon: Weapon) -> None:
        self._name = name
        self._weapon = weapon

    def attack(self):
        self._weapon.hit()


Dannerys = Warrior(
    "Dannerys Targerian, first of her name, king of the Andals, "
    "mother of the dragons, the unburnt, the chain breaker...",
    Weapon("sword", 90),
)
Dannerys.attack()

"""
Anonymous class
    Python doesn't really have anonymous classes, but there's a hack we can do
"""
anonymous_class = type(
    "",  # class name
    tuple(),  # parent classes
    {"user": "root@localhost"},  # attributes
)
print(anonymous_class.user)
# or you could simply do:
type("", tuple(), {"user": "root@localhost"}).user


# dataclass decorator to make class model implementation easier
@dataclass
class Person:
    _first_name: str
    _last_name: str
    _age: int

    # works like a getter
    @property
    def full_name(self):
        return self._first_name + " " + self._last_name

    # works like a setter
    @full_name.setter
    def full_name(self, full_name):
        raise ValueError("no needed")


Jao = Person(_first_name="Jao", _last_name="Pinto", _age=40)
print(asdict(Jao))
Jao.full_name = ""
