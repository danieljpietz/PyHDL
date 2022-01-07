import pytest
from pyhdl2 import *


def test_create_module():
    @module
    class MyModule(Module):

        clk = PortSignal("clk", std_logic, Direction.In)
        sig = Signal("sig", std_logic, std_logic(0))

        @process(clk)
        def my_proc(self):
            self.sig.next = self.sig.neg()

    print()
    print(Project(MyModule).value())
    print()
