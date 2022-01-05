from pyhdl2 import *

@entity
class ExampleEntity(Entity):
    interfaces = (PortSignal('clk', std_logic, Direction.In),
                  PortSignal('output', std_logic, Direction.Out))


@architecture
class ExampleArchitecture(Architecture):
    entity = ExampleEntity

    @record
    class MyRecord(Record):
        v: std_logic
        rst: std_logic

    record_signal = Signal("record_signal", MyRecord, default=MyRecord(std_logic(1), std_logic(0)))
    sig1 = Signal("sig1", std_logic, default=std_logic(0))

    @process(entity.clk)
    def my_process(self):
        @IF(self.entity.clk == std_logic('1'))
        def my_if():
            self.entity.output.next = self.sig1
            self.sig1.next = self.sig1.neg()


write_out(ExampleEntity, ExampleArchitecture, "getting_started.vhd")
