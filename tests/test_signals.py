import pytest
from pyhdl2 import *


def test_create_signal():
    my_sig = Signal("my_sig", std_logic)
    assert my_sig.value() == "my_sig"
    assert my_sig.serialize_declaration() == "my_sig : std_logic"

    my_sig2 = Signal("my_sig2", std_logic, std_logic('1'))
    assert my_sig2.serialize_declaration() == "my_sig2 : std_logic := \'1\'"


def test_signal_reserved_name():
    with pytest.raises(NameError):
        Signal("signal", std_logic)


def test_bad_default():
    with pytest.raises(TypeError):
        my_bad_sig = Signal("my_sig", std_logic, 2)


def test_signal_bad_index():
    my_sig = Signal("my_sig", std_logic)
    with pytest.raises(TypeError):
        my_sig[0]
    with pytest.raises(TypeError):
        len(my_sig)


def test_signal_array_indexing():
    my_signal_vector = Signal("vec", std_logic_vector(3, 0))
    for i in range(3):
        assert my_signal_vector[i].value() == f"vec({i})"
    assert (len(my_signal_vector) == 3)


def test_signal_arithmetic():
    sig1 = Signal("sig1", integer)
    sig2 = Signal("sig2", integer)
    sig4 = Signal("sig4", integer)
    sig3 = sig1 + sig2 + sig4 + (sig1 + sig2)
    assert sig3.value() == "sig1 + sig2 + sig4 + (sig1 + sig2)"
    sig4 = sig1 + integer(1) + (integer(2) + integer(3))
    assert sig4.value() == "sig1 + 1 + (2 + 3)"

    assert (sig1 + sig2).value() == 'sig1 + sig2'
    assert (sig1 - sig2).value() == 'sig1 - sig2'
    assert (sig1 * sig2).value() == 'sig1 * sig2'
    assert (sig1 / sig2).value() == 'sig1 / sig2'

    assert (sig1 & sig2).value() == 'sig1 and sig2'
    assert (sig1 | sig2).value() == 'sig1 or sig2'
    assert (sig1 ^ sig2).value() == 'sig1 xor sig2'

    assert (sig1 > sig2).value() == 'sig1 > sig2'
    assert (sig1 >= sig2).value() == 'sig1 >= sig2'
    assert (sig1 < sig2).value() == 'sig1 < sig2'
    assert (sig1 <= sig2).value() == 'sig1 <= sig2'

    assert (sig1 == sig2).value() == 'sig1 = sig2'
    assert (sig1 != sig2).value() == 'sig1 != sig2'
    assert (-sig1).value() == "-sig1"
    assert (sig1 == sig2).neg().value() == 'not (sig1 = sig2)'


def test_signal_arithmetic_op_check():
    sig1 = Signal("sig1", std_logic)
    sig2 = Signal("sig2", std_logic)

    with pytest.raises(TypeError):
        sig1 + sig2
