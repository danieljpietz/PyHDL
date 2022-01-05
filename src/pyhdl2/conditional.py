from typing import Callable, List, Union, Optional
from .core import _PHDLObj
from .type import isarray
from .architecture import Architecture
from .arithmetic import ArithmeticStack
from .process import Process, _get_current_process
from copy import deepcopy


class Conditional(_PHDLObj):

    def __init__(self, architecture: Architecture, process: Process, condition: Optional[ArithmeticStack]):
        self.architecture = architecture
        self.process = process
        if condition is None and not isinstance(self, Else):
            raise TypeError("Missing condition for if statement")
        self.condition = condition
        self.if_str = ''
        self.parent: Union[Process, Conditional, None] = None
        self.childrenStrings: List[str] = []
        self._if_strs: List[str] = []
        self.func: Callable[[], None]
        self._elses: List[str] = []
        pass

    def __call__(self, func: Callable[[], None]):
        # This is
        global ifStack
        self.parent = ifStack[-1] if len(ifStack) > 0 else self.process
        self.parent.add_if(self)
        self.func = func
        self.process_if()

        pass

    def process_if(self):
        global ifLast
        pre_signals = deepcopy(self.process.get_signals())
        ifStack.append(self)
        self.func()
        if not isinstance(self, Else):
            ifLast = self
        ifStack.pop()
        post_signals = self.process.get_signals()
        all_sigs = []
        for pre_signal, post_signal in zip(pre_signals, post_signals):
            if isarray(pre_signal.type):
                for pre_arr, pos_arr in zip(pre_signal, post_signal):
                    all_sigs.append((pre_arr, pos_arr))
            else:
                all_sigs.append((pre_signal, post_signal))
        for pre_signal, post_signal in all_sigs:
            if pre_signal.next is not None and post_signal.next is not None \
                    and pre_signal.next.value() != post_signal.next.value():
                raise ValueError("Cannot make assignment to value used in if statement")
            elif pre_signal.next is None and post_signal.next is not None:
                self._if_strs.append(f"\t{post_signal.name} <= {post_signal.next.value()};")
                post_signal.next = None

    def add_if(self, _if):
        self._if_strs.append(f"\n{_if.value()}")

    def add_else(self, _else):
        self._elses.append(f"{_else.value()}")

    def value(self):
        if self.condition is not None:
            nl = '\n'
            tab = '\t'
            self.if_str = f"\t{self.func.__name__}: if {self.condition.value()} then \n" \
                          f"{f'{nl}'.join(self._if_strs)}" \
                          f"{f'{nl}'.join(self._elses)}\n" \
                          f"end if {self.func.__name__};"
            self.if_str = self.if_str.replace(nl, f"{nl}{tab * (len(ifStack) + 1)}")
            return self.if_str
        pass


class Else(Conditional):
    def __init__(self, architecture: Architecture, process: Process, condition: Optional[ArithmeticStack],
                 parent: Optional[Conditional]):
        super().__init__(architecture, process, condition)
        self.parent: Conditional
        if self.parent is not None:
            self.parent = parent

    def __call__(self, func: Callable[[], None]):
        # This is
        self.func = func
        self.process_if()
        self.parent.add_else(self)
        pass

    def value(self):
        nl = '\n'
        tab = '\t'
        self.if_str = f"else {f'if {self.condition.value()} then' if self.condition is not None else ''} \n" \
                      f"{f'{nl}'.join(self._if_strs)}"
        self.if_str = self.if_str.replace(nl, f"{nl}{tab * (len(ifStack))}")
        return self.if_str


ifStack: List[Conditional] = []
ifLast: Optional[Conditional] = None


def IF(condition):
    return Conditional(_get_current_process().architecture, _get_current_process(), condition)


def ELSEIF(condition):
    global ifLast
    return Else(_get_current_process().architecture, _get_current_process(), condition, ifLast)


def ELSE():
    global ifLast
    return Else(_get_current_process().architecture, _get_current_process(), None, ifLast)