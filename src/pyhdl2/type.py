from abc import abstractmethod
import typing
from typing import Optional, Tuple, Dict, Any
from .arithmetic import Operable
from .check import check_name
from dataclasses import dataclass


class _Type:
    """Base class for all PHDL Types"""
    name: str
    type: type
    requires: Optional[Dict[str, Tuple[str]]] = None
    package: Optional[Any]
    subtype: Optional[Tuple[Any]]

    def __str__(self):
        return self.name

    def __new__(cls: typing.Type[Any], *_v):
        if not isrecord(cls):
            v = _v[0]
            if v is not None and not cls.__contains__(cls, v):
                raise ValueError(f"{v} not in the domain of {cls.name}")
            cls.type = cls
            return super(_Type, cls).__new__(cls)
        else:
            for expected, actual in zip(cls.__annotations__.values(), _v):
                if not isinstance(actual, expected):
                    raise TypeError(f"Unexpected type found in  record. Expected {expected} but got {actual}")
            pass


class Type(_Type, Operable):

    def __str__(self):
        return f"{self.name}({self.value()})"

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __init__(self, value: Any):  # pragma: no cover
        """ Create a version of the object with a concrete value """
        pass

    @abstractmethod
    def __contains__(self, item: Any) -> bool:  # pragma: no cover
        """ Returns true if the item is in the domain of this type """
        pass

    @abstractmethod
    def type_check(self, other: Any, op: str) -> type:  # pragma: no cover
        """ Returns true of the two values are compatible for the given operation """
        pass

    @abstractmethod
    def cast(self, other: typing.Type[Any]) -> bool:  # pragma: no cover
        """ Returns true if the other value can be casted to this type """
        pass

    @abstractmethod
    def value(self):  # pragma: no cover
        pass


class _Array(Type):
    bounds: Tuple[int, int] = (-1, -1)
    values: Optional[typing.List[Type]] = None

    def typestring(self):
        return f"type {self.name} is array of {self.base.name} " \
               f"({self.bounds[0]} {'down' if self.bounds[0] > self.bounds[1] else ''}to " \
               f"{self.bounds[1]});"


def isarray(cls):
    try:
        return issubclass(cls, _Array)
    except TypeError:
        return isinstance(cls, _Array)


def new_type(arg: typing.Type[Type]):
    for attr in ('type_check', 'cast', 'value', '__init__', '__contains__'):
        try:
            arg.__dict__[attr]
        except KeyError:
            if not issubclass(arg, Record):
                raise NotImplementedError(f"{arg} missing required attribute {attr}")
    arg.name = arg.__name__
    check_name(arg.name)
    return arg


def Array(_name: str, _base_type: typing.Type[Type], _bounds: Tuple[int, int],
          generic_bounds: Optional[bool] = False, **kwargs):
    class _arr(_Array):
        bounds = _bounds
        base = _base_type
        name = _name
        subtype = (_base_type,)
        if generic_bounds:
            name = f"{_name} ({bounds[0]} {'down' if bounds[0] > bounds[1] else ''}to {bounds[1]})"
        else:
            name = _name

        requires = kwargs['requires'] if 'requires' in kwargs else None

        if len(bounds) != 2:
            raise ValueError("Bounds must be a tuple of length 2")
        for b in bounds:
            if b < 0 or (int(b) != b):
                raise ValueError(f"Bounds must be a non-negative integer. Found {b}")

    check_name(_arr.name)
    return _arr


def record(arg):
    rec = dataclass(new_type(arg), eq=False)
    rec.subtype = get_subtypes_from_list(rec.__annotations__.values())
    return rec


class Record(_Type):

    def value(self):
        values = ','.join([f"{key} => {self.__dict__[key].value()}" for key in self.__annotations__])
        return f"({values})"

    def typestring(self):
        return f"type {self.__name__} is record\n\t" + \
               '\n\t'.join(
                   [f"{key} : {self.__annotations__[key].name};" for key in self.__annotations__]) \
               + f"\nend record {self.__name__};"

    pass


def isrecord(cls):
    try:
        return issubclass(cls, Record)
    except TypeError:
        return isinstance(cls, Record)


def generate_typestrings(types):
    for outer_custom_type in types:
        for inner_custom_type in types:
            if inner_custom_type is outer_custom_type:
                break
            elif inner_custom_type.name == outer_custom_type.name:
                if generate_typestring(inner_custom_type) != generate_typestring(outer_custom_type):
                    raise ValueError(f"Found multiple definitions for type {inner_custom_type.name}.")
    return '\n'.join(set([generate_typestring(custom_type) for custom_type in types]))
    pass


def generate_typestring(custom_type: Any):
    return custom_type.typestring(custom_type)


def get_subtypes_from_list(types):
    __types = []
    for _type in types:
        _types = get_subtypes_recursive(_type)
        for _t in reversed(_types):
            if _t not in __types:
                __types.append(_t)
    return __types


def get_subtypes_recursive(_type):
    subtypes = [_type]
    try:
        for sub in _type.subtype:
            subtypes += get_subtypes_recursive(sub)
    except AttributeError:
        pass
    finally:
        return subtypes
