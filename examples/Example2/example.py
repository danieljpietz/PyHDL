from pyhdl2 import *


@module
class MyModule(Module):

    clk = PortSignal("clk", std_logic, Direction.In)

    sig1 = Signal("sig1", integer)
    sig2 = Signal("sig2", integer)
    sig3 = Signal("sig3", integer)

    @RISING_EDGE(clk)
    def my_edge_detector(self):
        self.sig3.next = self.sig2 ^ self.sig1
        pass


write_out("MyModule.vhdl", MyModule)
