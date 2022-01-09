import pytest
from pyhdl2 import *


def test_function_creation():

    @function
    def my_function(self, arg1: std_logic, arg2: std_logic) -> std_logic:
        @IF(arg1)
        def my_if():
            self.output.next = arg2
        @ELSE()
        def my_else():
            self.output.next = arg1

    @module
    class MyModule(Module):
        sig = Signal("sig", std_logic)
        @process()
        def proc(self):
            self.sig.next = my_function(std_logic('1'), std_logic('0'))


def test_bad_func_call():
    with pytest.raises(TypeError):
        @function
        def my_function(self, arg1: std_logic, arg2: std_logic) -> std_logic:
            pass

        @module
        class MyModule(Module):
            sig = Signal("sig", std_logic)

            @process()
            def proc(self):
                self.sig.next = my_function(std_logic('1'), integer(3))

