import pytest
from pyhdl2 import *


@entity
class MyEntity(Entity):
    interfaces = (PortSignal("clk", std_logic, Direction.In),
                  PortSignal("rst", std_logic, Direction.In))


def test_create_architecture():
    @architecture
    class MyArchitecture(Architecture):
        entity = MyEntity

        sig = Signal("sig", std_logic)
        sig2 = Signal("sig2", std_logic_vector(0, 3))
        sig3 = Signal("sig3", std_logic_vector(3, 0))
        sig4 = Signal("sig4", Array("MyCustomType", std_logic, (0, 10)))
        sig5 = Signal("sig5", Array("MyCustomType2", std_logic, (10, 9)))

        @process(entity.clk)
        def my_process(self):
            self.sig2.next = self.sig
            self.sig3[1].next = self.sig & self.sig2 | (self.sig ^ self.sig2 & (self.sig3[2] | self.sig))

            @IF(self.entity.clk == std_logic(1))
            def my_if():
                self.sig3[0].next = self.sig3[1]

    print(MyArchitecture.value())
    MyArchitecture.value()


def test_architecture_forget_subclass():
    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(object):
            entity = MyEntity


def test_architecture_bad_entity():
    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            entity = 4


def test_architecture_bad_name():
    with pytest.raises(NameError):
        @architecture
        class MyBadlyNamedArchitecture(Architecture):
            entity = MyEntity
            name = "architecture"
