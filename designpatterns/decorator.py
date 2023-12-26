"""
this is a Decorator Design Pattern, do not confuse with the Django "signal",
although is similar
"""
from abc import ABC, abstractmethod


class DriverInterface(ABC):  # interface

    experience = 0
    category = "Noob"

    @abstractmethod
    def check_experience(self):
        raise NotImplementedError(
            "you have to implement 'check_experience' method"
        )


# d = DriverInterface() # can't be instantiated since is an abstract class


class DriverDecorator(DriverInterface, ABC):  # abstract decorator

    driver = None

    def __init__(self, driver: DriverInterface) -> None:
        self.driver = driver


# d = DriverDecorator() # can't be instantiated since is an abstract class


class noobDriver(DriverInterface):  # concrete class

    experience = 0
    category = "Noob"

    def check_experience(self) -> int:
        print(
            f"I'm a {self.category} driver with experience {self.experience}"
        )


class professionalDriver(DriverDecorator):  # concrete class

    experience = 50
    category = "Professional"

    def check_experience(self) -> int:
        self.driver.check_experience()
        print(
            f"I'm no longer a {self.driver.category}, now I'm a"
            f"{self.category} driver with experience {self.experience}"
        )


class AceDriver(DriverDecorator):  # concrete class

    experience = 100
    category = "Ace"

    def check_experience(self) -> int:
        self.driver.check_experience()
        print(
            f"I'm no longer a {self.driver.category}, now I'm a"
            f"{self.category} driver with experience {self.experience}"
        )


driver = noobDriver()
# driver.check_experience()
driver = professionalDriver(driver)
# driver.check_experience()
driver = AceDriver(driver)
driver.check_experience()
