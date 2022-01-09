from .architecture import architecture, Architecture
from .entity import entity, Entity
from .signal import PortSignal
from typing import Tuple, List


class Module(Architecture):
    interfaces: Tuple[PortSignal]


def get_interfaces_recursive(items):
    _items = []
    for item in items:
        if isinstance(item, PortSignal):
            _items.append(item)
        elif isinstance(item, List) and not isinstance(item, str):
            _items += get_interfaces_recursive(item)
    return _items




def module(cls):
    _interfaces = get_interfaces_recursive(list(cls.__dict__.values()))

    @entity
    class _ent(Entity):
        interfaces = tuple(_interfaces)
        name = cls.__name__
        pass

    cls.entity = _ent
    mod = architecture(cls)
    mod.value() # Checks are evaluated when this is run
    return mod
