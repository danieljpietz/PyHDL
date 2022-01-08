from .core import _PHDLObj, f_string_from_template, indent
from .type import generate_typestrings, _Type
from .signal import Constant
from .procedure import Procedure


class Package(_PHDLObj):
    def __init__(self, cls):
        self.name = cls.__name__
        self.elements = cls.elements
        self.types = []
        self.constants = []
        self.subprograms = []
        for elem in self.elements:
            elem.package = self
            elem.requires = {'work': f'{self.name}.all'}
            if isinstance(elem, Constant):
                self.constants.append(elem)
            elif isinstance(elem, Procedure):
                self.subprograms.append(elem)
            elif issubclass(elem, _Type):
                self.types.append(elem)

    def value(self):
        types = indent(generate_typestrings(self.types), 1)
        constants = indent('\n'.join([f'{const.serialize_declaration()};' for const in self.constants]), 1)
        procedures = ('\n\n'.join([proc.value() for proc in self.subprograms]))
        return f_string_from_template('package.vhdl',
                                      name=self.name,
                                      types=types,
                                      constants=constants,
                                      procedures=procedures)


def package(cls):
    return Package(cls)
