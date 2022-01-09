from typing import Callable, List, Optional
from .core import f_string_from_template, indent

from .architecture import Architecture
from .arithmetic import ArithmeticStack
from .process import _get_current_process
from .statements import Statements


class Conditional(Statements):

    def __init__(self, architecture: Architecture, condition: Optional[ArithmeticStack]):
        self.architecture = architecture
        if condition is None and not isinstance(self, Else):
            raise TypeError("Missing condition for if statement")
        self.condition = condition
        pass

    def __call__(self, func: Callable[[], None]):
        global ifLast
        ifLast = self
        self.set_function(func)
        self.set_signals(self.architecture.get_signals())
        self.set_args()
        self.parent()
        pass

    def value(self):
        if self.condition is not None:
            self.if_str = f_string_from_template('conditional.vhdl',
                                                 name=self.get_function_name(),
                                                 condition=self.condition.value(),
                                                 body=super(Conditional, self).value())
            self.if_str = indent(self.if_str, len(ifStack) + 1)
            return self.if_str
        else:
            raise AttributeError("Conditional Statement must contain a condition")


class Else(Conditional):
    def __init__(self, architecture: Architecture, condition: Optional[ArithmeticStack]):
        super().__init__(architecture, condition)

    def value(self):
        self.if_str = f"else {f'if {self.condition.value()} then' if self.condition is not None else ''} \n\n" \
                      f"{super(Conditional, self).value()}"
        self.if_str = indent(self.if_str, len(ifStack))
        return self.if_str


ifStack: List[Conditional] = []
ifLast: Optional[Conditional] = None


def _get_current_if():
    return ifStack[-1]


def IF(condition):
    return Conditional(_get_current_process().architecture, condition)


def ELSEIF(condition):
    global ifLast
    elsif = Else(_get_current_process().architecture, condition)
    ifLast.add_child(elsif)
    return elsif


def ELSE():
    global ifLast
    _else = Else(_get_current_process().architecture, None)
    return _else


def case(expression: ArithmeticStack):
    pass
