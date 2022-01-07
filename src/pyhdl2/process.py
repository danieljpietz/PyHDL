from .core import _PHDLObj, f_string_from_template
from typing import Optional, Tuple, List, Callable, Union, Any
from .signal import Signal, PortSignal, Direction, Constant
from .check import check_name


class Process(_PHDLObj):
    def __init__(self, sensitivity: Optional[Union[Tuple[Signal], Signal, None]] = None, label: Optional[str] = None):
        self.proc_str = None
        self.func: Callable[[_PHDLObj], None]
        self.sensitivity = sensitivity
        if label is None:
            self.name: str
        else:
            self.name = label
        self.proc_strs: List[str] = []
        self.proc_str: str
        self.if_statements: List[Process] = []
        self.architecture: Any

    def __call__(self, func: Callable[[_PHDLObj], None]):
        self.func = func
        if not hasattr(self, 'name'):
            self.name = self.func.__name__
        check_name(self.name)
        return self
        pass

    def invoke(self):
        _set_current_process(self)
        self.sanitize_signals()
        self.func(self.architecture)
        _set_current_process(None)
        self.process_signals()
        self.proc_str = ('\n'.join(self.proc_strs))
        self.architecture.processes.append(self)

    def sig_list(self):
        return self.architecture.signals + list(self.architecture.entity.interfaces)

    def process_signals(self):
        for signal in get_signals_from_list(self.sig_list()):
            if signal.next is not None:
                if isinstance(signal, PortSignal) and signal.direction == Direction.In:
                    raise TypeError("Cannot make assignment to input signal")
                elif isinstance(signal, Constant):
                    raise TypeError("Cannot make assignment to constant")
                self.process_signal(signal)

    def add_if(self, IF):
        self.if_statements.append(IF)

    def sanitize_signals(self):
        for signal in get_signals_from_list(self.sig_list()):
            if signal.next is not None:
                raise ValueError("No signals should have a next component outside of a process. "
                                 "You probably set it somewhere else in your architecture")

    def get_signals(self):
        return get_signals_from_list(self.sig_list())

    def process_signal(self, signal):
        if signal.next.type != signal.type:
            signal.next = signal.cast(signal.next)
        self.proc_strs.append(f"\t{signal.name} <= {signal.next.value()};")
        signal.next = None

    def add_procedure_call(self, proc):
        self.if_statements.append(proc)
        pass

    def value(self):
        _sensitivity = f"({', '.join([signal.name for signal in self.sensitivity])})" \
            if isinstance(self.sensitivity, tuple) \
            else f"({self.sensitivity.name})" if self.sensitivity is not None \
            else ""

        _ifs = '\n'.join([IF.value() for IF in self.if_statements])

        return f_string_from_template('process.vhdl',
                                      name=self.name,
                                      sensitivity=_sensitivity,
                                      body='\n'.join([self.proc_str, _ifs]))



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
