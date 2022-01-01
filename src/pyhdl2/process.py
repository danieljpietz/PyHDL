from .types import _PHDLObj, Signal
from typing import List, Optional, Callable
from collections.abc import Iterable


class Process(_PHDLObj):
    def __init__(self, func: Callable, sensitivity: Optional[List[Signal]]):
        self.func = func
        self.sensitivity = sensitivity
        self.name = None
        self.proc_strs = []
        self.proc_str = []

    def __call__(self, *args, **kwargs):
        self.func = args[0]
        self.name = self.func.__name__
        return self
        pass

    def invoke(self):
        for signal in self.architecture.signals:
            if signal.next is not None:
                raise ValueError("No signals should have a next component outside of a process. "
                                 "You probably set it somewhere else in your architecture")
        self.func(self.architecture)
        for signal in self.architecture.signals:
            if signal.next is not None:
                if not type(signal.next) in signal.type.casts:
                    if not isinstance(signal.next, signal.type) and not issubclass(signal.next.type, signal.type):
                        raise TypeError(f"Type {type(signal.next)} incompatible with {type(signal)}")
                    else:
                        # TODO: Typecasting
                        pass
                self.proc_strs.append(f"\t{signal.name} <= {signal.next.value()};")
            signal.next = None
        self.proc_str = ('\n'.join(self.proc_strs))
        self.architecture.processes.append(self)
        pass

    def serialize(self):
        _sensitivity = f"({', '.join([signal.name for signal in self.sensitivity])})" \
            if isinstance(self.sensitivity, Iterable) \
            else f"({self.sensitivity.name})" if self.sensitivity is not None \
            else ""

        _ser = f"{self.name}: process {_sensitivity}\n" \
               f"begin \n" \
               f"{self.proc_str}\n" \
               f"end process;"
        return _ser


def process(sig=None):
    def wrapper(self):
        return self
    return Process(wrapper, sig)
