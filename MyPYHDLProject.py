from pyhdl2 import *


@entity
class MyEntity(Entity):
    interfaces = [PortSignal("clk", std_logic, Direction.In), PortSignal("output", std_logic, Direction.Out)]


@architecture
class MyArchitecture(Architecture):
    entity = MyEntity

    sig = Signal("sig", integer)
    sig2 = Signal("sig2", integer)
    sig_vec = Signal("sig_vec", std_logic_vector((0, 4)))
    custom = Signal("custom", array("MyArray", integer, (0, 5)))

    @process(entity.clk)
    def my_process(self):
        self.sig.next = self.sig * self.sig2
        self.custom[0].next = self.custom[1]

        @IF(self.my_process, self.sig == self.sig2)
        def first_if():
            self.custom[1].next = self.custom[0]
            pass

        pass


