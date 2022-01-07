from .architecture import architecture, Architecture
from .entity import entity, Entity
from .signal import PortSignal
from typing import Tuple


class Module(Architecture):
    interfaces: Tuple[PortSignal]


def module(cls):

    _interfaces = []

    for sig in cls.__dict__.values():
        if isinstance(sig, PortSignal):
            _interfaces.append(sig)


    @entity
    class _ent(Entity):
        interfaces = tuple(_interfaces)
        name = cls.__name__
        pass

    cls.entity = _ent

    return architecture(cls)