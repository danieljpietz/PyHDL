from pyhdl2 import *


@module
class MyModule(Module):
    clk = PortSignal("clk", std_logic, Direction.In)

    @RISING_EDGE(clk)
    def behavior(self):
        pass


write_out("MyModule.vhdl", MyModule)
