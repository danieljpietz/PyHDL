import pytest
from pyhdl2 import *

def test_enum():
    TestEnum = Enum("TestEnum", "State1", "State2", "State3")

    @module
    class MyMod(Module):

        sig = Signal("sig", TestEnum)

    pass