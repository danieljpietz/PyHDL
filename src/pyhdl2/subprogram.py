from .signal import PortSignal
from .architecture import Architecture, _architecture, get_architecture_processes, get_architecture_types
from .check import check_name
from .process import Process
from .entity import Entity
from typing import Tuple


class _Procedure(Process):

    def __init__(self, func):
        self.func = func
        super(_Procedure, self).__init__()


class Procedure(Architecture):
    interfaces: Tuple[PortSignal]

    def value(self):
        proc = self.processes[0]
        _interfaces = self.entity.interface_string(self.entity)
        return f"procedure {self.__class__.__name__} ({_interfaces}) is \n" \
               f"{self.signals_string()}\n" \
               f"begin\n" \
               f"{proc.proc_str}\n" \
               f"end procedure {self.__class__.__name__};"


def procedure(_target):
    target = _target()
    if not issubclass(_target, Procedure):
        raise TypeError(f"Procedure {_target} must inherit Procedure")
    if not hasattr(_target, 'interfaces'):
        raise AttributeError(f"Procedure {_target} must declare interfaces")
    check_name(_target.__name__)

    class _entity(Entity):
        interfaces = _target.interfaces

    target.entity = _entity
    _architecture(target)
    _target.proc = _Procedure(_target.invoke)
    get_architecture_processes(target)
    get_architecture_types(target)
    return target
