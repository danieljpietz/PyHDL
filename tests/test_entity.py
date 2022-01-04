import pytest

from pyhdl2 import *


def test_create_entity():
    @entity
    class MyEntity(Entity):
        interfaces = ()

    assert MyEntity.name == "MyEntity"

    @entity
    class MyEntity2(Entity):
        name = "MyEntity2"
        interfaces = ()

    assert MyEntity2.name == "MyEntity2"


def test_entity_no_subclass():
    with pytest.raises(TypeError):
        @entity
        class MyEntity(object):
            interfaces = ()

def test_serialize_entity():
    @entity
    class MyEntity(Entity):
        interfaces = (PortSignal("clk", std_logic, Direction.In),)
    assert MyEntity.value() == 'entity MyEntity is\n\t port (clk : in std_logic);\nend entity MyEntity;'


def test_create_entity_bad_name():
    with pytest.raises(NameError):
        @entity
        class eNtItY(Entity):
            interfaces = ()

    with pytest.raises(NameError):
        @entity
        class MyBadEntity(Entity):
            name = "sIgNaL"
            interfaces = ()

