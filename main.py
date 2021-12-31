from pyhdl2 import *


@module
class MyModule(Module):
    interfaces = [PortSignal("clk", std_logic, Direction.In)]


@architecture
class MyArchitecture(Architecture):
    module = MyModule
    signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(10)]

    @process([signalVectors[0]])
    def my_process(self):
        pass

    pass

print(MyArchitecture)
