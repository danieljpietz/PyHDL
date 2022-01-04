import pytest
from pyhdl2 import *


def test_new_type():
    @new_type
    class MyNewType(Type):
        def __init__(self, value):
            pass

        def __contains__(self, item):
            pass

        def value(self):
            pass

        def type_check(self, other, op):
            pass

        def cast(self, other):
            pass


def test_type_reserved_name():
    with pytest.raises(NameError):
        @new_type
        class signal(Type):
            def __init__(self, value):
                pass

            def __contains__(self, item):
                pass

            def value(self):
                pass

            def type_check(self, other, op):
                pass

            def cast(self, other):
                pass


def test_out_of_domain():
    with pytest.raises(ValueError):
        std_logic('2')


def test_neg_incomplete_type():
    with pytest.raises(NotImplementedError):
        @new_type
        class my_incomplete_type(Type):
            def __init__(self):
                pass

            def __contains__(self, item):
                pass

            def type_check(self, other, op):
                pass


def test_neg_bad_array_bounds():
    with pytest.raises(ValueError):
        my_bad_type = Array("name", std_logic, (-1, 0))
    with pytest.raises(ValueError):
        my_bad_type = Array("name", std_logic, (0.1, 0))
    with pytest.raises(ValueError):
        my_bad_type = Array("name", std_logic, (0, 10, 20))


def test_index_array():
    myType = Array('myType', std_logic, (10, 0))

    thing = Signal("thing", myType)

    assert thing[0].value() == "thing(0)"

    with pytest.raises(IndexError):
        thing[11].value()