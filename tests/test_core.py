import pytest
from pyhdl2 import *


def test_bad_name_check():
    with pytest.raises(TypeError):
        Signal(1, std_logic)
