from pyhdl2 import *

@procedure
class MyProcedure(Procedure):
    interfaces = (PortSignal("a", std_logic, Direction.In),
                  PortSignal("b", std_logic, Direction.In),
                  PortSignal("c", std_logic, Direction.Out))

    sig = Signal("sig", std_logic)

    def invoke(self):
        @IF(rising_edge(self.a))
        def my_if():
            self.c.next = self.a & self.b

        @ELSE()
        def my_else():
            self.c.next = self.a | self.b


@function
def myFunction(self, arg1: std_logic) -> std_logic:
    self.output.next = arg1

@package
class MyPackage:
    elements = [MyProcedure, myFunction]


@module
class MyModule(Module):

    input1 = Signal("input1", std_logic)
    input2 = Signal("input2", std_logic)
    output = Signal("output", std_logic)

    @process()
    def proc(self):
        MyProcedure(self.input1, self.input2, self.output)


write_out("PackagesProcedures.vhdl", MyModule)