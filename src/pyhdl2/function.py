from .procedure import Procedure, procedure
from inspect import signature
from .signal import PortSignal, Direction, Signal
from .check import check_name
from .core import f_string_from_template, indent
from .process import _get_current_process
from .statements import Statements

class _FunctionCall(Signal):
    def __init__(self, func: Procedure, args):
        self.func = func
        self.args = args
        self.type = func.interfaces[-1].type

    def value(self):
        return f"{self.func.__class__.__name__}" \
               f"({', '.join([f'{actual.value()}' for expected, actual in zip(self.func.interfaces[:-1], self.args)])}); "


def function(_target):
    params = signature(_target).parameters
    ret_type = signature(_target).return_annotation
    _interfaces = []
    for name, _type in zip(params, params.values()):
        _interfaces.append(PortSignal(name, _type.annotation, Direction.In))
    _interfaces.append(PortSignal("output", ret_type, Direction.Out))
    check_name(_target.__name__)


    class Function(Statements):
        #interfaces = _interfaces[1:]

        def __init__(self, func, scope):
            self.set_function(func)
            self.set_signals(scope)
            self.interfaces = _interfaces[1:-1]
            self.set_args(*tuple([self] + self.interfaces))


        def invoke(self):
            _target(self, *tuple(self.interfaces[:-1]))
            pass

        def value(self):
            args = f", ".join([f"{signal.name} : {signal.type.name}" for signal in self.interfaces])
            return f_string_from_template('function.vhdl',
                                          name=_target.__name__,
                                          args=args,
                                          ret_type=ret_type.name,
                                          body=indent(super(Function, self).value(), 1)).replace("output <=", "return")

        def __call__(self, *args, **kwargs):
            for found, expected in zip(args, self.interfaces):
                if found.type != expected.type:
                    raise TypeError(f"Unexpected type for {found.name}. "
                                    f"Expected {expected.type.name}, found {found.type.name}")
            try:
                if self.package is not None:
                    _get_current_process().architecture.add_element_libs_and_packs(self)
            except AttributeError:
                pass
            return _FunctionCall(self, args)

    Function.__class__.__name__ = _target.__name__
    return Function(_target, _interfaces)
