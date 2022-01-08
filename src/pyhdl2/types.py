import typing
from typing import Any, Dict, Tuple
from .type import Type, new_type, Array


@new_type
class std_logic(Type):
    requires = {'IEEE': ('std_logic_1164.all',)}

    def __init__(self, value):
        self._value = value

    def __contains__(self, item):
        return str(item) in ('0', '1', 'X')

    def value(self):
        return f"\'{self._value}\'"

    def type_check(self, other, op):
        if op in ('and', 'or', 'not', 'xor', '=', '!='):
            return std_logic
        else:
            raise TypeError(f"Operation {op} incompatible with type std_logic")
        pass

    def cast(self, other):
        return self
        pass


def std_logic_vector(bound1: int, bound2: int):
    return Array('std_logic_vector', std_logic, (bound1, bound2), requires={'IEEE': ('std_logic_1164.all',)},
                 generic_bounds=True)


@new_type
class integer(Type):
    casts = ()
    requires: Dict[str, Tuple[str]] = {}

    def __init__(self, value):
        self._value = int(value)

    def __contains__(self, item):
        return isinstance(item, (int, integer))

    def value(self):
        return f"{self._value}"

    def type_check(self, other: Any, op: str) -> type:
        return integer

    def cast(self, other: typing.Type[Any]) -> bool:
        pass

