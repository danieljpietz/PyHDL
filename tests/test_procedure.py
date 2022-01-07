import pytest
from pyhdl2 import *


def test_create_procedure():
    @procedure
    class MyProcedure(Procedure):

        interfaces = (PortSignal("a", std_logic, Direction.In),
                      PortSignal("b", std_logic, Direction.In),
                      PortSignal("c", std_logic, Direction.Out))

        sig = Signal("sig", std_logic)

        def invoke(self):
            self.c.next = self.a & self.b
    pass



def test_create_bad_procedure():
    with pytest.raises(AttributeError):
        @procedure
        class MyProcedure(Procedure):
            def invoke(self):
                pass

def test_prcedure_typecheck():
    with pytest.raises(TypeError):
        @procedure
        class MyProcedure(Procedure):
            interfaces = (PortSignal("a", std_logic, Direction.In),
                          PortSignal("b", std_logic, Direction.In),
                          PortSignal("c", std_logic, Direction.Out))

            sig = Signal("sig", std_logic)

            def invoke(self):
                self.c.next = self.a & self.b

        pass

        @module
        class MyMod(Module):
            input1 = Signal("input1", std_logic)
            input2 = Signal("input2", integer)
            output = Signal("output", std_logic)

            @process()
            def proc(self):
                MyProcedure(self.input1, self.input2, self.output)

def test_call_procedure():
    @procedure
    class MyProcedure(Procedure):
        interfaces = (PortSignal("a", std_logic, Direction.In),
                      PortSignal("b", std_logic, Direction.In),
                      PortSignal("c", std_logic, Direction.Out))

        sig = Signal("sig", std_logic)

        def invoke(self):
            self.c.next = self.a & self.b

    pass

    @module
    class MyMod(Module):

        input1 = Signal("input1", std_logic)
        input2 = Signal("input2", std_logic)
        output = Signal("output", std_logic)

        @process()
        def proc(self):
            MyProcedure(self.input1, self.input2, self.output)

    MyMod.value()
    pass