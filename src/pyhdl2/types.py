from dataclasses import dataclass
from enum import IntEnum
import typing
from typing import Tuple, List, Optional, Dict
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
    casts: Optional[Tuple[typing.TypeVar('T')]] = None
    requires: Optional[Dict] = None

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
    bounds: Optional[Tuple[int, int]] = None
    values: Optional[List] = None

    def __index__(self, ind):
        if ind < min(self.bounds) or ind >= max(self.bounds):
            raise IndexError(f"Index {ind} is out of range {self.bounds}")
        print('x')

    def serialize(self):
        return f"{self.name} ({max(self.bounds)} downto {min(self.bounds)})"


@dataclass
class SignalBase(_PHDLObj):

    def __init__(self, name: str, type: Type):
        self.name = name
        self.type = type
        self.next: SignalBase = None
        if issubclass(self.type, Array):
            self.values = [Signal(f"{self.name}({i})", self.type.type) for i in
                           range(min(self.type.bounds), max(self.type.bounds))]

    def serialize(self):
        return f"{self.name} : {self.type.serialize(self.type)}"

    def __getitem__(self, item):
        if issubclass(self.type, Array):
            return self.values[item]
            pass
        else:
            raise TypeError(f"Cannot index non array type {self.type}")

    def __len__(self):
        if issubclass(self.type, Array):
            return len(self.values)
            pass
        else:
            raise TypeError(f"Cannot index non array type {self.type}")

    def __add__(self, other):
        return operator(self, other, '+')

    def __sub__(self, other):
        return operator(self, other, '-')

    def __mul__(self, other):
        return operator(self, other, '*')

    def __and__(self, other):
        return operator(self, other, 'and')

    def __or__(self, other):
        return operator(self, other, 'or')

    def __xor__(self, other):
        return operator(self, other, 'xor')

    def __ne__(self, other):
        return operator(self, other, '!=', conditional=True)

    def __eq__(self, other):
        return operator(self, other, '=', conditional=True)

    def __gt__(self, other):
        return operator(self, other, '>', conditional=True)

    def __lt__(self, other):
        return operator(self, other, '<', conditional=True)

    def __ge__(self, other):
        return operator(self, other, '>=', conditional=True)

    def __le__(self, other):
        return operator(self, other, '<=', conditional=True)


class SigNode(Node, SignalBase):

    def value(self):
        if len(self.children) == 2:
            return f"({self.children[0].value()} {self.name} {self.children[1].value()})"
        elif len(self.children) == 1:
            return f"{self.name} ({self.children[0].value()})"
            pass
        elif len(self.children) == 0:
            return self.name

    pass


class Condition(SigNode):
    pass


def operator(left, right, op, conditional=False):
    if conditional:
        NodeClass = Condition
    else:
        NodeClass = SigNode

    nodes = [left, right]
    op_node = NodeClass(op)
    op_node.type = left.type.type_check(left.type, right.type, op)
    for node in nodes:
        if isinstance(node, NodeClass):
            node.parent = op_node
        elif isinstance(node, SignalBase) or isinstance(node, Type):
            NodeClass(node.value(), parent=op_node)
        else:
            raise TypeError(f"Unexpected type {type(node)}. Expected SigNode, SignalBase, or Type")
    return op_node
    pass


@dataclass
class Signal(SignalBase):
    SignalBase.type: Type = None

    def __init__(self, name: str, _type: str, default: Optional[SignalBase.type] = None):
        super().__init__(name, _type)

        if not isinstance(default, _type) and default is not None:
            raise TypeError(f'Unexpected type for default (expected {_type} but found {type_(default)})')

        self.default = default

    def __eq__(self, other):
        return SignalBase.__eq__(self, other)

    def value(self):
        return self.name

    def serialize(self):
        return f"{SignalBase.serialize(self)}{f' := {self.default.value()}' if self.default is not None else f''}"


class Direction(IntEnum):
    In = 0,
    Out = 1,
    InOut = 2

    def __str__(self):
        return ['in', 'out', 'inout'][self]


@dataclass
class PortSignal(SignalBase):

    def __init__(self, name: str, _type: Type, direction: Direction):
        super().__init__(name, _type)
        self.direction = direction

    def value(self):
        if self.direction != Direction.Out:
            return self.name
        else:
            raise TypeError("Cannot read value from output pin")


def type_(arg):
    arg.type_str = arg.__name__
    return arg


@type_
class std_logic(Type):
    casts = ()
    requires = {'IEEE': ['std_logic_1164.all']}

    def __init__(self, value):
        self._value = value

    def __contains__(self, item):
        return str(item) in ['0', '1', 'X']

    def value(self):
        return f"\'{self._value}\'"


def array(_name, base_type, range, **kwargs):
    class _arr(Array):
        bounds = range
        type = base_type
        name = _name
        if 'requires' in kwargs:
            requires = kwargs['requires']

    return _arr


def std_logic_vector(_bounds: Tuple[int, int]):
    return array("std_logic_vector", std_logic, _bounds, requires={})


@type_
class integer(Type):
    casts = ()
    requires = {}

    def __init__(self, value):
        self._value = int(value)

    def __contains__(self, item):
        return isinstance(item, (int, integer))

    def value(self):
        return f"{self._value}"
