import pytest
from pyhdl2 import *


def test_create_package():

    @record
    class MyRecord(Record):
        v: std_logic
        v1 = std_logic_vector(0, 3)

    @package
    class MyPackage:
        elements = [Array("MyArray", std_logic, (0, 3)), MyRecord]
        pass

    @entity
    class Ent(Entity):
        interfaces = (PortSignal("input", MyRecord, Direction.In),)

    @architecture
    class Arch(Architecture):
        entity = Ent

    print()
    print(MyPackage.value())

    x = Project(Ent, Arch)
    print(x)

    pass