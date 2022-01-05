import pytest
from pyhdl2 import *

def test_create_record():

    @new_type
    class MyRecord(Record):
        v: std_logic
        v1: std_logic_vector(3, 0)
        pass

    @entity
    class MyEnt(Entity):
        interfaces = (PortSignal('clk', std_logic, Direction.In),)

    @architecture
    class MyArch(Architecture):
        entity = MyEnt

        sig = Signal("sig", MyRecord)

    print()
    print(MyArch.value())
    print()