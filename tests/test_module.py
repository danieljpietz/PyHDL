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


def test_array_signals():
    @module
    class MyModule(Module):

        clk = PortSignal("clk", std_logic, Direction.In)

        signals = [Signal("sig1", std_logic, std_logic(0)),
                   Signal("sig2", std_logic, std_logic(0)),
                   Signal("sig3", std_logic, std_logic(0))]

        @process(clk)
        def my_proc(self):
            @IF(rising_edge(self.clk))
            def my_if():
                self.sig1.next = std_logic('1')

    print()
    print(MyModule.value())
    print()