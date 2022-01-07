from .type import _Type
from .types import std_logic
from .check import check_name

def Enum(name, values):

    check_name(name)
    for arg in values:
        check_name(arg)

    class _Enum(_Type):
        type_name = name
        elements = values
        def __init__(self, val):
            self._value = val
            pass

        def __contains__(self, item):
            return item in self.elements

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
            return f"type {self.type_name} is ({', '.join(self.elements)});"
            pass
        pass
    _Enum.type = _Enum
    return _Enum