import pytest
from pyhdl2 import *


def test_create_module():
    @module
    class MyModule(Module):

        clk = PortSignal("clk", std_logic, Direction.In)
        sig = Signal("sig", std_logic, std_logic(0))

        @process(clk)
        def my_proc(self):
            @IF(self.clk == std_logic('1'))
            def my_if():
                self.sig.next = self.sig.neg()

            @ELSEIF(self.clk == std_logic('0'))
            def my_elsif():
                self.sig.next = self.sig

            @ELSE()
            def my_else():
                self.sig.next = self.clk

    print()
    print(Project(MyModule).value())
    print()
