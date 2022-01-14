from pyhdl2 import *


@module
class MyModule(Module):
    sig = Signal("sig", integer)
    sig1 = Signal("sig1", integer)
    sig2 = Signal("sig2", integer)
    clk = PortSignal("clk", std_logic, Direction.In)

    @RISING_EDGE(clk)
    def my_proc(self):
        self.sig2.next = self.sig + self.sig1 + self.sig2 + self.sig2 + self.sig1
        smx_optimizer(self, self.sig2)


write_out("SMX.vhdl", MyModule)
