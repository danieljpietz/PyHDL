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
        sig2 = Signal("sig2", std_logic)

        @process()
        def my_process(self):
            self.sig.v.next = self.sig2
            self.sig2.next = self.sig2.neg()


    print()
    print(MyArch.value())
    print()