from dataclasses import dataclass
from enum import IntEnum
import typing
from typing import Tuple, Callable
from abc import ABC, abstractmethod
from contextlib import suppress
from functools import wraps
import inspect


class _PHDLObj(ABC):
    @abstractmethod
    def serialize(self):
        # raise TypeError("Object \'_PHDL\' must be subclassed before it is serialized")
        pass

    def __str__(self):
        return self.serialize()


def enforce_types(callable):
    spec = inspect.getfullargspec(callable)

    def check_types(*args, **kwargs):
        parameters = dict(zip(spec.args, args))
        parameters.update(kwargs)
        for name, value in parameters.items():
            with suppress(KeyError):  # Assume un-annotated parameters can be any type
                type_hint = spec.annotations[name]
                if isinstance(type_hint, typing._SpecialForm):
                    # No check for typing.Any, typing.Union, typing.ClassVar (without parameters)
                    continue
                try:
                    actual_type = type_hint.__origin__
                except AttributeError:
                    # In case of non-typing types (such as <class 'int'>, for instance)
                    actual_type = type_hint
                # In Python 3.8 one would replace the try/except with
                # actual_type = typing.get_origin(type_hint) or type_hint
                if isinstance(actual_type, typing._SpecialForm):
                    # case of typing.Union[…] or typing.ClassVar[…]
                    actual_type = type_hint.__args__

                if not isinstance(value, actual_type):
                    raise TypeError(
                        'Unexpected type for \'{}\' (expected {} but found {})'.format(name, type_hint, type(value)))

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_types(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    if inspect.isclass(callable):
        callable.__init__ = decorate(callable.__init__)
        return callable

    return decorate(callable)


@enforce_types
@dataclass
class Type(_PHDLObj):
    type: str

    def serialize(self):
        return self.type


@enforce_types
@dataclass
class Array(Type):
    bounds: Tuple[int, int]

    def serialize(self):
        return f"{self.type} ({max(self.bounds)} downto {min(self.bounds)})"


@enforce_types
@dataclass
class Signal(_PHDLObj):
    name: str
    type: Type

    def serialize(self):
        return f"{self.name} : {self.type}"


class Direction(IntEnum):
    In = 0,
    Out = 1,
    InOut = 2

    def __str__(self):
        return ['in', 'out', 'inout'][self]


@enforce_types
@dataclass
class PortSignal(Signal):
    direction: Direction


std_logic = Type("std_logic")
std_logic_vector: Callable[[int, int], Array] = lambda b1, b2: Array("std_logic_vector", (b1, b2))
