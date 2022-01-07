from .core import _PHDLObj, f_string_from_template, indent
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
        types = indent(generate_typestrings(self.types), 1)
        constants = indent('\n'.join([f'{const.serialize_declaration()};' for const in self.constants]), 1)
        return f_string_from_template('package.vhdl',
                                      name=self.name,
                                      types='\t' + types,
                                      constants='\t' + constants)


def package(cls):
    return Package(cls)
