from abc import abstractmethod
import typing
from typing import Optional, Tuple, Dict, Any
from .arithmetic import Operable
from .check import check_name


class _Type:
    """Base class for all PHDL Types"""
    type_name: str
    type: type
    requires: Optional[Dict[str, Tuple[str]]] = None

    def __str__(self):
        return self.type_name


class Type(_Type, Operable):

    def __new__(cls: typing.Type[Any], v: Any=None):
        if v is not None and not cls.__contains__(cls, v):
            raise ValueError(f"{v} not in the domain of {cls}")
        cls.type = cls
        return super(Type, cls).__new__(cls)

    def __str__(self):
        return f"{self.type_name}({self.value()})"

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
    arg.type_name = arg.__name__
    check_name(arg.type_name)
    return arg


def Array(_name: str, _base_type: typing.Type[Type], _bounds: Tuple[int, int],
          generic_bounds: Optional[bool] = False, **kwargs):
    class _arr(_Array):
        bounds = _bounds
        base = _base_type
        name = _name
        if generic_bounds:
            type_name = f"{_name} ({bounds[0]} {'down' if bounds[0] > bounds[1] else ''}to {bounds[1]})"
        else:
            type_name = _name

        requires = kwargs['requires'] if 'requires' in kwargs else None

        if len(bounds) != 2:
            raise ValueError("Bounds must be a tuple of length 2")
        for b in bounds:
            if b < 0 or (int(b) != b):
                raise ValueError(f"Bounds must be a non-negative integer. Found {b}")

    check_name(_arr.name)
    return _arr


class Record(_Type):
    pass


def isrecord(cls):
    try:
        return issubclass(cls, Record)
    except TypeError:
        return isinstance(cls, Record)


def record_typestring(custom_type: Any):
    return f"type {custom_type.__name__} is record\n\t" + \
           '\n\t'.join(
               [f"{key} : {custom_type.__annotations__[key].type_name};" for key in custom_type.__annotations__]) \
           + f"\nend record {custom_type.__name__};"



def generate_typestrings(types):
    for outer_custom_type in types:
        for inner_custom_type in types:
            if inner_custom_type is outer_custom_type:
                break
            elif inner_custom_type.type_name == outer_custom_type.type_name:
                if generate_typestring(inner_custom_type) != generate_typestring(outer_custom_type):
                    raise ValueError(f"Found multiple definitions for type {inner_custom_type.name}.")
    return '\n'.join(set([generate_typestring(custom_type) for custom_type in types]))
    pass


def generate_typestring(custom_type: Any):
    if not isrecord(custom_type):
        return f"type {custom_type.name} is array of {custom_type.base.type_name} " \
               f"({custom_type.bounds[0]} {'down' if custom_type.bounds[0] > custom_type.bounds[1] else ''}to " \
               f"{custom_type.bounds[1]});" if isarray(custom_type) else ''
    else:
        return record_typestring(custom_type)
