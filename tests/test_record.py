import pytest
from pyhdl2 import *


def test_create_record():
    @record
    class MyRecord(Record):
        v: std_logic
        v1: std_logic
        pass

    x = MyRecord(std_logic('1'), std_logic('0'))

    @entity
    class MyEnt(Entity):
        interfaces = (PortSignal('clk', std_logic, Direction.In),)
    pass

    @architecture
    class MyArch_Record(Architecture):
        entity = MyEnt

        sig = Signal("sig", MyRecord)
        sig2 = Signal("sig2", std_logic)

        @process()
        def my_process(self):
            self.sig.v.next = self.sig2
            self.sig2.next = self.sig2.neg()


def test_record_typecheck():
    with pytest.raises(TypeError):
        @record
        class MyRecord(Record):
            v: std_logic
            v1: std_logic
            pass

        x = MyRecord(std_logic('1'), integer(3))
