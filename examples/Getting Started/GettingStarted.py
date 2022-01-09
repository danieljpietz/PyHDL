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


@module
class GettingStarted(Module):
    clk = PortSignal('clk', std_logic, Direction.In)
    output = PortSignal('output', std_logic, Direction.Out)

    record_signal = Signal("record_signal", MyRecord, default=MyRecord(std_logic(1), std_logic(0)))
    sig1 = Signal("sig1", std_logic, default=std_logic(0))

    vector = Signal("vector", std_logic_vector(0, 10))

    my_other_const = Constant("my_other_const", std_logic, std_logic('1'))

    @process(clk)
    def my_process(self):
        @IF(rising_edge(self.clk))
        def my_if():
            self.entity.output.next = self.sig1
            self.sig1.next = Const


write_out("getting_started.vhd", GettingStarted)
