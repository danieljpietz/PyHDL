from .process import process
from .architecture import Architecture
from .signal import Signal, PortSignal, Direction
from .types import std_logic
from .enum import Enum, elements_of
from .conditional import IF
from .module import module, Module
from .statements import Statements


class State(Statements):

    def __init__(self, func):
        self.set_function(func)
        self.architecture: Architecture
        pass


def state(_func):
    return State(func=_func)


class FSM(Module):
    clk = PortSignal("clk", std_logic, Direction.In)
    states: Enum
    state: Enum


def fsm_behavior(self):
    for state, _state in zip(elements_of(self.states), self.architecture.States):
        _state.set_signals(self.get_signals())
        _state.set_types(self.architecture.types)
        def fsm_if(state):
            state.parent()

        func = IF(self.state == state)
        func(fsm_if)
        func.args = _state,
    pass


def fsm(cls):
    _states = list(filter(lambda CLS: isinstance(CLS, State), cls.__dict__.values()))
    cls.states = Enum("states", [state.get_function().__name__ for state in _states])
    cls.state = Signal("state", cls.states)
    cls.States = _states
    cls.fsm_behavior = process(cls.clk)(fsm_behavior)
    return module(cls)
