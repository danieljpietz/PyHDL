from .core import _PHDLObj
from .signal import PortSignal, Direction, Constant
from abc import abstractmethod


class Statements(_PHDLObj):
    children = []
    types = []
    components = []
    def __init__(self, scope, function):
        self.args = (self,)
        self.architecture = None
        self.__signals = scope
        self.__function = function
        self.add_attrs()
        self.statement_strings = []
        self.statement_string = ''
        self.children = []
        self.types = []
        self.components = []
        self.parent()

    def reset(self):
        self.add_attrs()
        self.statement_strings = []
        self.statement_string = ''
        self.children = []
        self.parent()
        if not hasattr(self, 'args'):
            self.args = (self,)

    def parent(self):
        if get_current_statement() is not None and self not in get_current_statement().children:
            get_current_statement().children.append(self)

    def set_args(self, *args):
        self.args = args

    def set_architecture(self, arch):
        self.architecture = arch

    def get_architecture(self):
        return self.architecture

    def set_function(self, func):
        self.__function = func

    def get_function(self):
        return self.__function

    def get_function_name(self):
        return self.get_function().__name__

    def set_signals(self, signals):
        self.__signals = signals

    def get_signals(self):
        return self.__signals

    def set_types(self, types):
        self.types = types

    def get_types(self):
        return self.types

    def set_components(self, components):
        self.components = components

    def get_components(self):
        return self.components

    def add_attrs(self):
        for element in list(self.get_signals()) + list(self.get_types()) + list(self.get_components()):
            setattr(self, element.name, element)

    def process_signals(self):
        for signal in get_signals_from_list(self.get_signals()):
            if signal.next is not None:
                if isinstance(signal, PortSignal) and signal.direction == Direction.In:
                    raise TypeError("Cannot make assignment to input signal")
                elif isinstance(signal, Constant):
                    raise TypeError("Cannot make assignment to constant")
                self.process_signal(signal)

    def add_child(self, child):
        self.children.append(child)

    def process_signal(self, signal):
        if signal.next.type != signal.type:
            signal.next = signal.cast(signal.next)
        self.statement_strings.append(f"\t{signal.name} <= {signal.next.value()};")
        signal.next = None

    #@abstractmethod
    def value(self):
        self.reset()
        set_current_statement(self)
        self.get_function()(*self.args)
        decrement_stack()
        self.process_signals()
        self.statement_string = '\n'.join([child.value() for child in self.children]) + \
                                '\n'.join(self.statement_strings)
        return self.statement_string


_callStack = []


def set_current_statement(statement):
    global _callStack
    _callStack.append(statement)


def decrement_stack():
    global _callStack
    _callStack = _callStack[:-1]


def get_current_statement():
    global _callStack
    if len(_callStack) > 0:
        return _callStack[-1]
    else:
        return None


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
