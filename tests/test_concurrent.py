import pytest
from pyhdl2 import *


def test_concurrent():
    @module
    class MyModule(Module):
        clk = PortSignal("clk", std_logic, Direction.In)

        sig1 = Signal("sig1", std_logic)
        sig2 = Signal("sig2", std_logic)

        @concurrent
        def concurrent_section(self):
            self.sig1.next = self.clk

    print()
    print(MyModule.value())
    print()