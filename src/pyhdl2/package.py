from .core import _PHDLObj
from .type import generate_typestrings, _Type
from .signal import Constant

class Package(_PHDLObj):
    def __init__(self, cls):
        self.name = cls.__name__
        self.elements = cls.elements
        for elem in self.elements:
            elem.package = self
            elem.requires = {'work': f'{self.name}.all'}
        pass
        self.types = []
        self.constants = []
        for elem in self.elements:
            if isinstance(elem, Constant):
                self.constants.append(elem)
            elif issubclass(elem, _Type):
                self.types.append(elem)
        pass




    def value(self):
        nl = '\n'
        return f"package {self.name} is \n" \
               f"{generate_typestrings(self.types)} \n" \
               f"{f'{nl}'.join([f'{const.serialize_declaration()};' for const in self.constants])}" \
               f"end package {self.name};\n"


def package(cls):
    return Package(cls)