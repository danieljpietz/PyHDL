import pytest
from pyhdl2 import *


def test_generate_module(tmpdir):
    @entity
    class MyEntity(Entity):
        interfaces = (PortSignal("clk", std_logic, Direction.In),
                      PortSignal("input", std_logic, Direction.In),
                      PortSignal("output", std_logic, Direction.Out))

    @architecture
    class MyArchitecture(Architecture):
        entity = MyEntity

        sig_vec = Signal("sig_vec", std_logic_vector(0, 4))

        @process(MyEntity.clk)
        def my_process(self):
            @IF(MyEntity.clk)
            def first_if():
                for i in range(len(self.sig_vec)):
                    self.sig_vec[i].next = self.sig_vec[i - 1]
                self.sig_vec[-1].next = MyEntity.input

    file = tmpdir.join('output.vhd')
    write_out(file.strpath, MyEntity, MyArchitecture)
