from .core import _PHDLObj
from typing import Optional, Tuple, List, Callable, Union, Any
from .type import isarray, isrecord
from .signal import Signal, PortSignal, Direction
from .check import check_name


class Process(_PHDLObj):
    def __init__(self, sensitivity: Optional[Union[Tuple[Signal], Signal, None]] = None):
        self.func: Callable[[_PHDLObj], None]
        self.sensitivity = sensitivity
        self.name: str
        self.proc_strs: List[str] = []
        self.proc_str: str
        self.if_statements: List[Process] = []
        self.architecture: Any

    def __call__(self, func: Callable[[_PHDLObj], None]):
        self.func = func
        self.name = self.func.__name__
        check_name(self.name)
        return self
        pass

    def get_signals(self):
        return self.architecture.signals + list(self.architecture.entity.interfaces)

    def invoke(self):
        _set_current_process(self)
        self.sanitize_signals()
        self.func(self.architecture)
        _set_current_process(None)

        for signal in self.get_signals():
            if isarray(signal.type):
                for sig in signal:
                    if sig.next is not None:
                        if isinstance(signal, PortSignal) and signal.direction == Direction.In:
                            raise TypeError("Cannot make assignment to input signal")
                        self.process_signal(sig)
            elif isrecord(signal.type):
                for key in signal.type.__annotations__:
                    sig = signal.__dict__[key]
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

    def add_if(self, IF):
        self.if_statements.append(IF)

    def sanitize_signals(self):
        for signal in self.get_signals():
            if isarray(signal.type):
                for sig in signal:
                    if sig.next is not None:
                        raise ValueError("No signals should have a next component outside of a process. "
                                         "You probably set it somewhere else in your architecture")
            if signal.next is not None:
                raise ValueError("No signals should have a next component outside of a process. "
                                 "You probably set it somewhere else in your architecture")

    def process_signal(self, signal):
        if signal.next.type != signal.type:
            signal.next = signal.cast(signal.next)
        self.proc_strs.append(f"\t{signal.name} <= {signal.next.value()};")
        signal.next = None

    def value(self):
        _sensitivity = f"({', '.join([signal.name for signal in self.sensitivity])})" \
            if isinstance(self.sensitivity, tuple) \
            else f"({self.sensitivity.name})" if self.sensitivity is not None \
            else ""

        _ifs = '\n'.join([IF.value() for IF in self.if_statements])

        _ser = f"{self.name}: process {_sensitivity}\n" \
               f"begin \n" \
               f"{self.proc_str}\n" \
               f"{_ifs}" \
               f"end process;"
        return _ser


_currentProcess: Optional[Process]


def _set_current_process(proc: Optional[Process]):
    global _currentProcess
    _currentProcess = proc


def _get_current_process():
    global _currentProcess
    return _currentProcess


def process(sig=None):
    return Process(sig)
