import pytest
from pyhdl2 import *

def test_process_input_assignment():
    with pytest.raises(TypeError):
        @entity
        class MyEnt(Entity):
            interfaces = (PortSignal("a", std_logic, Direction.In),
                          PortSignal("b", std_logic, Direction.In),
                          PortSignal("c", std_logic, Direction.Out))

        @architecture
        class MyArch(Architecture):
            entity=MyEnt
            @process()
            def myProc(self):
                self.a.next = self.b


def test_process_output_read():
    with pytest.raises(TypeError):
        @entity
        class MyEnt(Entity):
            interfaces = (PortSignal("a", std_logic, Direction.In),
                          PortSignal("b", std_logic, Direction.In),
                          PortSignal("c", std_logic, Direction.Out))

        @architecture
        class MyArch(Architecture):
            entity = MyEnt
            @process()
            def myProc(self):
                self.c.next = self.c