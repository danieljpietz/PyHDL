import pytest
from pyhdl2 import *


def test_std_logic():
    for value in ([0, 1, '0', '1', 'X']):
        x = std_logic(value)
        assert str(x) == f"std_logic(\'{str(value)}\')"
        assert repr(x) == str(x)


def test_std_logic_domain_error():
    with pytest.raises(ValueError):
        std_logic(2)


def test_std_logic_vector():
    x = std_logic_vector(0, 3)
    assert x.type_name == "std_logic_vector (0 to 3)"
    x = std_logic_vector(3, 0)
    assert x.type_name == "std_logic_vector (3 downto 0)"


def test_std_logic_vector_bad_index():
    with pytest.raises(ValueError):
        std_logic_vector(-1, 0)

    with pytest.raises(ValueError):
        std_logic_vector(0.1, 1)
