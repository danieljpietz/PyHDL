from .type import _Type
from .types import std_logic
from .check import check_name

def Enum(_name, values):

    check_name(_name)
    for arg in values:
        check_name(arg)

    class _Enum(_Type):
        name = _name
        _elements = values

        def __init__(self, val):
            self._value = val
            pass

        def __contains__(self, item):
            return item in self._elements

        def value(self):
            return self._value

        def type_check(self, other, op):
            if op in ['=', '!=']:
                return std_logic
            else:
                raise TypeError("Cannot perform operation on enum")

        def cast(self, value):
            raise TypeError("Cannot cast enum")

        def typestring(self):
            return f"type {self.name} is ({', '.join(self._elements)});"
            pass
        pass

        def __getitem__(self, item):
            return _Enum(self._elements[item])

    _Enum.type = _Enum
    return _Enum


def elements_of(cls):
    return [cls(element) for element in cls._elements]