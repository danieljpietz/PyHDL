import pytest
from pyhdl2 import *

@module
class MyModule(Module):
    clk = PortSignal("clk", std_logic, Direction.In)
    rst = PortSignal("rst", std_logic, Direction.In)
    output = PortSignal("output", std_logic, Direction.Out)


def test_create_component():

    @module
    class otherModule(Module):
        clk = PortSignal("clk", std_logic, Direction.In)
        rst = PortSignal("rst", std_logic, Direction.In)
        output = PortSignal("output", std_logic, Direction.Out)

        test_component = Component("test_component", MyModule)

        @concurrent
        def concurrent_section(self):
            self.output.next = self.clk
            for x in range(10):
                self.test_component(self.clk, self.rst, self.output)


    otherModule.value()
    pass


def test_create_component_typecheck():

   with pytest.raises(TypeError):
       test_component = Component("test_component", MyModule)
       wrong_type = Signal("wrong_type", integer, Direction.Out)
       @concurrent
       def concurrent_section(self):
           self.test_component(self.clk, self.rst, wrong_type)