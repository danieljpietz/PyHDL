from .arithmetic import ArithmeticStack
from .signal import Signal, PortSignal, Direction
from .statements import Statements
from .process import Process, process
from .types import std_logic
from .enum import Enum, elements_of
from .conditional import IF, ELSEIF, ELSE
from copy import copy, deepcopy
from collections import deque

def smx_optimize_signal(signal: ArithmeticStack, depth=0, name=""):
    index = 0
    stacks = ArithmeticStack()
    new_signals = []
    it = iter(signal.next)
    if len(signal.next.stack) % 2:
        stack = ArithmeticStack()
        (item, op) = next(it)
        index = optimizer_inner_loop(depth, index, item, name, op, stack, new_signals)
        stacks.add(stack, '')

    for (item, op) in it:
        stack = ArithmeticStack()
        for _ in range(2):
            if not _:
                first_op = op
                op = ''
            index = optimizer_inner_loop(depth, index, item, name, op, stack, new_signals)
            if not _:
                (item, op) = next(it)
        stacks.add(stack, first_op)

    signal.next = stacks
    if len(stacks.stack) > 1:
        stacks, _new_signals = smx_optimize_signal(signal, depth + 1, name)
        new_signals += _new_signals
    if not depth:
        new_signals = new_signal_descrambler(new_signals)
    return stacks, new_signals


def new_signal_descrambler(signals):
    new_signals = []
    depth_signals = []
    depth_last = -1
    for (depth, signal) in reversed(signals):
        if depth != depth_last:
            new_signals.append(depth_signals)
            depth_signals = []
        depth_last = depth
        depth_signals.append(signal)
    new_signals.append(depth_signals)
    return new_signals[1:]


def optimizer_inner_loop(depth, index, item, name, op, stack, new_signals):
    if not isinstance(item, ArithmeticStack):
        stack.add(item, op)
    else:
        temp_signal = Signal(f"{name}{depth}{index}", item.type)
        temp_signal.next = item
        new_signals.append((depth, temp_signal))
        index += 1
        stack.add(temp_signal, op)
    return index


def smx_process_factory(new_signals, statements, states):
    new_signals = deepcopy(new_signals)
    def smx_process(self):
        for signals, statement, state in zip(new_signals, statements, elements_of(states)):
            statement.set_signals(signals)
            def _if():
                statement.parent()
            func = IF(self.smx_state == state)
            func.args = statement,
            func.set_signals(statement.get_signals())
            func(_if)
    return Statements([], smx_process)


def smx_optimizer(arch: Process, signal: ArithmeticStack):
    _, new_signals = smx_optimize_signal(signal, 0, name=signal.name)
    new_signals = deque(new_signals)
    new_signals.appendleft([signal])
    new_signals = list(new_signals)
    statements = []

    for sigs in new_signals:
        s = Statements(sigs, lambda _: None)
        s.set_signals(sigs)
        statements.append(s)
        pass

    arch.smx_states = Enum(f"{signal.name}_smx_states", [f"{signal.name}_smx_states_{i}" for i in range(len(statements) + 1)])
    arch.smx_state = Signal("smx_state", arch.smx_states)

    S = smx_process_factory(new_signals, statements, arch.smx_states)
    S.set_signals(arch.get_signals() + [arch.smx_state])
    S.parent()

    pass
