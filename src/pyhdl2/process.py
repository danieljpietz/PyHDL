from .types import _PHDLObj, Signal, PortSignal, Direction, Array
from typing import List, Optional, Callable
from collections.abc import Iterable
import itertools

class Process(_PHDLObj):
    def __init__(self, func: Callable[[], None], sensitivity: Optional[List[Signal]] = None):
        self.func = func
        self.sensitivity = sensitivity
        self.name: str
        self.proc_strs: List[str] = []
        self.proc_str: str

    def __call__(self, *args, **kwargs):
        self.func = args[0]
        self.name = self.func.__name__
        return self
        pass

    def invoke(self):
        for signal in list(itertools.chain(*[self.architecture.signals, self.architecture.entity.interfaces])):
            if issubclass(signal.type, Array):
                for sig in signal:
                    if sig.next is not None:
                        raise ValueError("No signals should have a next component outside of a process. "
                                         "You probably set it somewhere else in your architecture")
                pass
            if signal.next is not None:
                raise ValueError("No signals should have a next component outside of a process. "
                                 "You probably set it somewhere else in your architecture")
        self.func(self.architecture)
        for signal in list(itertools.chain(*[self.architecture.signals, self.architecture.entity.interfaces])):
            if issubclass(signal.type, Array):
                for sig in signal:
                    if sig.next is not None:
                        if isinstance(signal, PortSignal) and signal.direction == Direction.In:
                            raise TypeError("Cannot make assignment to input signal")
                        self.process_signal(sig)
            else:
                if signal.next is not None:
                    if isinstance(signal, PortSignal) and signal.direction == Direction.In:
                        raise TypeError("Cannot make assignment to input signal")
                    self.process_signal(signal)

        self.proc_str = ('\n'.join(self.proc_strs))
        self.architecture.processes.append(self)
        pass

    def process_signal(self, signal, array=True):
        if not type(signal.next) in signal.type.casts:
            if not isinstance(signal.next, signal.type) and not issubclass(signal.next.type, signal.type):
                raise TypeError(f"Type {type(signal.next)} incompatible with {type(signal)}")
            else:
                # TODO: Typecasting
                pass

            self.proc_strs.append(f"\t{signal.name} <= {signal.next.value()};")
        signal.next = None

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
