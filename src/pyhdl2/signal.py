from .type import isarray, isrecord
from typing import Union, Tuple, Any, Type
from abc import abstractmethod
from .arithmetic import Operable
from enum import IntEnum
from .check import check_name


class _Signal(Operable):
    next: Union[Any, None] = None
    def __init__(self, name: str, signal_type, **kwargs):
        self.name = name
        check_name(self.name)
        self.type = signal_type
        self.next: _Signal
        if isarray(self.type):
            self.values = [Signal(f"{self.name}({i})", self.type.base) for i in
                           range(min(self.type.bounds), max(self.type.bounds))]
        elif isrecord(self.type):
            for key in self.type.__annotations__:
                setattr(self, key, Signal(f"{self.name}.{key}", self.type.__annotations__[key]))


    @abstractmethod
    def value(self):
        pass

    def __repr__(self):
        return f"{type(self)}({self.value()})"

    def __getitem__(self, item):
        if isarray(self.type):
            return self.values[item]
        else:
            raise TypeError(f"Cannot index non array type {self.type}")

    def __len__(self):
        if isarray(self.type):
            return len(self.values)
            pass
        else:
            raise TypeError(f"Cannot index non array type {self.type}")


class Signal(_Signal):

    def __init__(self, name: str, _type: Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]], default=None):
        super().__init__(name, _type)

        if default is not None and not isinstance(default, _type):
            raise TypeError(f'Unexpected type for default (expected {_type} but found {type(self).__name__})')
        self.default = default


    def value(self):
        return self.name

    def serialize_declaration(self):
        return f"{self.value()} : {self.type.type_name}" \
               f"{f' := {self.default.value()}' if self.default is not None else f''}"


class Direction(IntEnum):
    In = 0,
    Out = 1,
    InOut = 2

    def __str__(self):
        return ['in', 'out', 'inout'][self]


class PortSignal(_Signal):

    def __init__(self, name: str, _type: Type[Any], direction: Direction):
        super().__init__(name, _type)
        self.direction = direction

    def __repr__(self):
        return f"{type(self)}({self.value(skip_direction_check=True)})"

    def value(self, skip_direction_check=False):
        if skip_direction_check or self.direction != Direction.Out:
            return self.name
        else:
            raise TypeError("Cannot read value from output pin")
