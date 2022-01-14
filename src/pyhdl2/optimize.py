from .arithmetic import ArithmeticStack
from .signal import Signal
from collections.abc import Iterable
from .process import Process, process
from .conditional import IF, ELSEIF, ELSE
from anytree import Node, RenderTree

def smx_optimize_signal(signal: ArithmeticStack):

    it = iter(signal)

    stacks = []

    for _stack in it:
        stack = ArithmeticStack()
        stack.add(*_stack)
        stack.add(*next(it))
        stacks.append(stack)

    for stack in stacks:
        pass





    pass

def smx_optimizer(signals: ArithmeticStack):

    smx_optimize_signal(signals)

    pass
