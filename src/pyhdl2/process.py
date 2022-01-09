from .core import _PHDLObj, f_string_from_template
from typing import Optional, Tuple, Callable, Union, Any
from .signal import Signal
from .check import check_name
from .statements import Statements


class Process(Statements):
    def __init__(self, sensitivity: Optional[Union[Tuple[Signal], Signal, None]] = None, label: Optional[str] = None):
        self.proc_str = None
        self.func: Callable[[_PHDLObj], None]
        self.sensitivity = sensitivity
        if label is None:
            self.name: str
        else:
            self.name = label
        self.architecture: Any

    def __call__(self, func: Callable[[_PHDLObj], None]):
        if not hasattr(self, 'name'):
            self.name = func.__name__
        check_name(self.name)
        self.set_function(func)
        return self
        pass

    def sanitize_signals(self):
        for signal in get_signals_from_list(self.get_signals()):
            if signal.next is not None:
                raise ValueError("No scope should have a next component outside of a process. "
                                 "You probably set it somewhere else in your architecture")

    def _get_signals(self):
        return get_signals_from_list(self.get_signals())

    def value(self):
        self.sanitize_signals()
        _set_current_process(self)
        _sensitivity = f"({', '.join([signal.name for signal in self.sensitivity])})" \
            if isinstance(self.sensitivity, tuple) \
            else f"({self.sensitivity.name})" if self.sensitivity is not None \
            else ""

        return f_string_from_template('process.vhdl',
                                      name=self.name,
                                      sensitivity=_sensitivity,
                                      body=super(Process, self).value())


_currentProcess: Optional[Process]


def get_signals_from_list(signals):
    signalsOld = []
    signalsNew = signals
    while len(signalsOld) != len(signalsNew):
        signalsOld = signalsNew
        signalsNew = []
        for signal in signalsOld:
            try:
                for sig in signal:
                    signalsNew.append(sig)
            except TypeError:
                signalsNew.append(signal)
    return signalsNew


def _set_current_process(proc: Optional[Process]):
    global _currentProcess
    _currentProcess = proc


def _get_current_process():
    global _currentProcess
    return _currentProcess


def process(sig=None, label=None):
    return Process(sig, label)
