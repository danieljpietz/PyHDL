from pyhdl2 import *

@entity
class MyEntity(Entity):
    interfaces = [PortSignal("clk", std_logic, Direction.In)]


@architecture
class MyArchitecture(Architecture):
    entity = MyEntity

    sig = Signal("sig", std_logic)
    signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(4)]

    @process(sig)
    def my_process(self):
        self.sig.next = std_logic(0)
        pass

    @process(sig)
    def my_process2(self):
        self.sig.next = self.sig + self.signalVectors[0]
        pass
