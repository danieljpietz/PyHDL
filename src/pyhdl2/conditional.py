from abc import ABC
from typing import Callable
from .types import _PHDLObj, SigNode, Array
from .pyhdl import Architecture
from .process import Process
from copy import deepcopy


class Conditional(_PHDLObj, ABC):

    def __call__(self, func: Callable[[], None]):
        # This is
        pre_signals = deepcopy(self.process.get_signals())
        func()
        post_signals = self.process.get_signals()

        _if_str = ""

        for pre_signal, post_signal in zip(pre_signals, post_signals):
            if issubclass(pre_signal.type, Array):
                for pre_arr, pos_arr in zip(pre_signal, post_signal):
                    if pre_arr.next is not None and pre_arr.next.value() != pos_arr.next.value():
                        raise ValueError("Cannot make assignment to value used in if statement")
                    elif pos_arr.next is not None:
                        # Add to string
                        pass
            if pre_signal.next is not None and pre_signal.next.value() != post_signal.next.value():
                raise ValueError("Cannot make assignment to value used in if statement")
            elif post_signal.next is not None:
                # Add to string
                pass


    def serialize(self):

        pass

    def __init__(self, architecture: Architecture, process: Process, condition: SigNode):
        self.architecture = architecture
        self.process = process
        self.condition = condition

        pass


def IF(process, condition):
    return Conditional(process.architecture, process, condition)
