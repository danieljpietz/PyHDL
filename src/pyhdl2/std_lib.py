from .types import *
from .function import function
from .process import process, Process
from .conditional import IF
from .check import check_name


@function
def rising_edge(self, sig: std_logic) -> std_logic:
    pass


@function
def falling_edge(self, sig: std_logic) -> std_logic:
    pass


class _rising_edge_proc(Process):
    def __init__(self, sig):
        super(_rising_edge_proc, self).__init__(sig)
        self.set_function(self.func)
        self.ogFunc = None
        self._rising__edge__sign_l = sig

    def __call__(self, func):
        if not hasattr(self, 'name'):
            self.name = func.__name__
        check_name(self.name)
        self.ogFunc = func
        return self
        pass

    def func(self, *args):
        @IF(rising_edge(self._rising__edge__sign_l))
        def _if():
            self.ogFunc(self.get_architecture())
            pass
        pass
    pass


def RISING_EDGE(sig):
    return _rising_edge_proc(sig)
