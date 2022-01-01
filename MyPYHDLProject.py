from pyhdl2 import *


@entity
class MyEntity(Entity):
    interfaces = [PortSignal("clk", std_logic, Direction.In), PortSignal("output", std_logic, Direction.Out)]


@architecture
class MyArchitecture(Architecture):
    entity = MyEntity

    sig = Signal("sig", std_logic)
    sig_vec = Signal("sig_vec", std_logic_vector((0, 4)))
    #signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(4)]

    @process(entity.clk)
    def my_process(self):
        self.output.next = self.clk + self.clk + self.clk
        self.sig_vec[0].next = self.sig_vec[1]
        pass
