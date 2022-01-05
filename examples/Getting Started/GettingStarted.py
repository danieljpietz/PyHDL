from pyhdl2 import *


@entity
class ExampleEntity(Entity):
    interfaces = (PortSignal('clk', std_logic, Direction.In),
                  PortSignal('output', std_logic, Direction.Out))


@architecture
class ExampleArchitecture(Architecture):
    entity = ExampleEntity

    sig1 = Signal("sig1", std_logic, default=std_logic('0'))

    @process(entity.clk)
    def my_process(self):
        @IF(self.entity.clk == std_logic(0))
        def my_if():
            self.entity.output.next = self.sig1

        @ELSEIF(self.entity.clk == std_logic(1))
        def my_elseif():
            self.entity.output.next = std_logic(0)

        @ELSE()
        def my_else():
            self.entity.output.next = self.sig1


write_out(ExampleEntity, ExampleArchitecture, "getting_started.vhd")
