from dataclasses import dataclass
from enum import IntEnum
import typing
from typing import Tuple, Callable, Optional, Type
from abc import abstractmethod
from contextlib import suppress
from functools import wraps
import inspect
from anytree import Node


# from .parse import operator

class _PHDLObj(object):
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
                        'Unexpected type for \'{}\' (expected {} but found {})'.format(name, type_hint, type_(value)))

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


@dataclass
class Type(_PHDLObj):
    type_str: str
    casts: Optional[Tuple[Type]]

    def __new__(cls, v):
        if not cls.__contains__(cls, v):
            raise ValueError(f"{v} not in the domain of {cls}")
        return super(Type, cls).__new__(cls)
        pass

    def __str__(self):
        return f"{self.type_str}(\'{self.value}\')"

    def __repr__(self):
        return f"{type_(self).__name__ if hasattr(self, '__name__') else ''}(type_str=\'{self.type_str}\', value=\'{self.value()}\')"

    def serialize(self):
        return self.type_str

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def type_check(self, other, op):
        return self


@enforce_types
@dataclass
class Array(Type):
    bounds: Tuple[int, int]

    def serialize(self):
        return f"{self.type} ({max(self.bounds)} downto {min(self.bounds)})"


@dataclass
class _SignalBase(_PHDLObj):
    name: str
    type: Type

    def serialize(self):
        return f"{self.name} : {self.type.serialize(self.type)}"

    def __add__(self, other):
        return operator(self, other, '+')

    def __and__(self, other):
        return operator(self, other, 'and')

    def __or__(self, other):
        return operator(self, other, 'or')

    def __xor__(self, other):
        return operator(self, other, 'xor')

    def __sub__(self, other):
        return operator(self, other, '-')


class SigNode(Node, _SignalBase):

    def value(self):
        if len(self.children) >= 2:
            children = []
            for child in self.children:
                if len(child.children) == 2:
                    children.append(f"({child.value()})")
                else:
                    children.append(child.value())
            return f"{children[0]} {self.name} {children[1]}"
        elif len(self.children) == 1:
            return f"{self.name} ({self.children[0].value()})"
            pass
        elif len(self.children) == 0:
            return self.name
    pass


def operator(left, right, op):
    nodes = [left, right]
    op_node = SigNode(op)
    op_node.type = left.type.type_check(left.type, right.type, op)
    for node in nodes:
        if isinstance(node, SigNode):
            node.parent = op_node
        elif isinstance(node, _SignalBase) or isinstance(node, Type):
            SigNode(node.value(), parent=op_node)
        else:
            raise TypeError(f"Unexpected type {type(node)}. Expected SigNode, _SignalBase, or Type")
    return op_node
    pass


@dataclass
class Signal(_SignalBase):
    _SignalBase.type = None

    def __init__(self, name, _type, default: Optional[_SignalBase.type] = None):
        # TODO: Type checking for name and type
        self.name = name
        self.type = _type
        self.next = None

        if default is not None and not isinstance(default, _type):
            raise TypeError(f'Unexpected type for default (expected {_type} but found {type_(default)})')

        self.default = default

    def value(self):
        return self.name

    def serialize(self):
        return f"{_SignalBase.serialize(self)}{f' := {self.default.value()}' if self.default is not None else f''}"


class Direction(IntEnum):
    In = 0,
    Out = 1,
    InOut = 2

    def __str__(self):
        return ['in', 'out', 'inout'][self]


@dataclass
class PortSignal(_SignalBase):
    direction: Direction = None


def type_(arg):
    arg.type_str = arg.__name__
    return arg


@type_
class std_logic(Type):
    casts = ()

    def __init__(self, value):
        self._value = value

    def __contains__(self, item):
        return str(item) in ['0', '1', 'X']

    def value(self):
        return f"\'{self._value}\'"




std_logic_vector: Callable[[int, int], Array] = lambda b1, b2: Array("std_logic_vector", (b1, b2))
