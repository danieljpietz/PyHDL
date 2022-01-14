import pytest
from pyhdl2 import *


def test_stack_optimize():
    sig = Signal("sig1", integer)
    sig1 = sig - sig - sig - sig * sig - sig - sig

    smx_optimizer(sig1)

    pass