from .core import _PHDLObj
from .type import generate_typestrings


class Package(_PHDLObj):
    def __init__(self, cls):
        self.elements = cls.elements
        self.name = cls.__name__
        pass

    def value(self):
        return f"package {self.name} is \n" \
               f"{generate_typestrings(self.elements)} \n" \
               f"end package {self.name};\n"



def package(cls):
    return Package(cls)