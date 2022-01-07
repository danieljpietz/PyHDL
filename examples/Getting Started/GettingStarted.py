from pyhdl2 import *


@record
class MyRecord(Record):
    v: std_logic
    rst: std_logic


Const = Constant("MyConstant", MyRecord, MyRecord(std_logic('1'), std_logic('0')))


@package
class MyPackage:
    elements = [Array("MyArray", std_logic, (0, 3)), MyRecord,
                Const]
    pass


@module
class GettingStarted(Module):

    clk = PortSignal('clk', std_logic, Direction.In)
    output = PortSignal('output', std_logic, Direction.Out)

    record_signal = Signal("record_signal", MyRecord, default=MyRecord(std_logic(1), std_logic(0)))
    sig1 = Signal("sig1", std_logic, default=std_logic(0))

    @process(clk)
    def my_process(self):
        @IF(self.clk == std_logic('1'))
        def my_if():
            self.entity.output.next = self.sig1
            self.sig1.next = Const


write_out("getting_started.vhd", GettingStarted)
