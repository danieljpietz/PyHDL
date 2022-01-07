import pytest
from pyhdl2 import *

def test_enum():
    TestEnum = Enum("TestEnum", ("State1", "State2", "State3"))

    @module
    class MyMod(Module):

        sig = Signal("sig", TestEnum)


def test_enum_compare():
    @module
    class EnumExample(Module):
        EnumType = Enum("EnumType", ("Option1", "Option2", "Option3"))

        sig = Signal("sig", EnumType, EnumType("Option1"))

        @process()
        def my_process(self):
            @IF(self.sig == self.EnumType("Option1"))
            def state_check():
                self.sig.next = self.EnumType("Option2")

            pass

    EnumExample.value()