from .core import _PHDLObj, f_string_from_template, indent
from .signal import PortSignal
from .architecture import Architecture, _architecture, get_architecture_processes, get_architecture_types
from .check import check_name
from .process import Process, _get_current_process
from .entity import Entity
from typing import Tuple
from .conditional import _get_current_if


class _Procedure(Process):

    def __init__(self, func):
        self.func = func
        super(_Procedure, self).__init__()


class Procedure(Architecture):
    interfaces: Tuple[PortSignal]
    package = None

    def value(self):
        proc = self.processes[0]
        _interfaces = self.entity.interface_string(self.entity)

        return f_string_from_template('procedure.vhdl',
                                      name=self.__class__.__name__,
                                      interfaces=_interfaces,
                                      declarations=indent(self.signals_string(), 1),
                                      body=indent(proc.get_body(), 1))

    def __call__(self, *args, **kwargs):
        for found, expected in zip(args, self.interfaces):
            if found.type != expected.type:
                raise TypeError(f"Unexpected type for {found.name}. "
                                f"Expected {expected.type.type_name}, found {found.type.type_name}")
        if self.package is not None:
            _get_current_process().architecture.add_element_libs_and_packs(self)
        try:
            _get_current_if().add_procedure_call(_ProcedureCall(self, args))
        except IndexError:
            _get_current_process().add_procedure_call(_ProcedureCall(self, args))



class _ProcedureCall(_PHDLObj):
    def __init__(self, proc: Procedure, args):
        self.proc = proc
        self.args = args

    def value(self):
        return f"{self.proc.__class__.__name__} " \
               f"({', '.join([f'{expected.name} => {actual.value()}' for expected, actual in zip(self.proc.interfaces, self.args)])}); "


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
