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
