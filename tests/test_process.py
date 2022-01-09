import pytest
from pyhdl2 import *

def test_process_input_assignment():
    with pytest.raises(TypeError):
        @module
        class MyModule(Module):
            a = PortSignal("a", std_logic, Direction.In)
            b = PortSignal("b", std_logic, Direction.In)
            c = PortSignal("c", std_logic, Direction.Out)

            @process()
            def myProc(self):
                self.a.next = self.b


def test_process_output_read():
    with pytest.raises(TypeError):
        @module
        class MyThing(Module):
            a = PortSignal("a", std_logic, Direction.In),
            b = PortSignal("b", std_logic, Direction.In)
            c = PortSignal("c", std_logic, Direction.Out)
            @process()
            def myProc(self):
                self.c.next = self.c


def test_create_processes():
    @module
    class MyModule(Module):
        clk = PortSignal("clk", std_logic, Direction.In)
        sig = Signal("sig", std_logic)
        @process(clk)
        def my_process(self):
            self.sig.next = self.clk
