import pytest
from pyhdl2 import *


def test_create_module():
    @module
    class MyModule(Module):
        name = "MyModuleName"
        interfaces = None

    @module
    class MyModuleName(Module):
        interfaces = None

    assert MyModule.name == MyModuleName.name

    with pytest.raises(TypeError):
        @module
        class MyModule(Module):
            name = None
            interfaces = None

    with pytest.raises(TypeError):
        @module
        class MyModule(Module):
            interfaces = 1

    with pytest.raises(AttributeError):
        @module
        class MyModule(Module):
            name = "Name"
            pass

    with pytest.raises(TypeError):
        @module
        class PoorlyDerivedModule(int):
            interfaces = None

    with pytest.raises(TypeError):
        @module
        class WrongSignalType(Module):
            interfaces = ["NotAPortSignal"]

    @module
    class MyModule(Module):
        interfaces = None

    assert MyModule.serialize() == "entity MyModule is\n\t port ();\nend entity MyModule;"


def test_create_architecture():
    @module
    class MyModule(Module):
        interfaces = None

    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            module = None

    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            module = MyModule
            sig = PortSignal("sig", std_logic, Direction.In)

    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            module = MyModule

        MyArchitecture.add_signal(1)

    with pytest.raises(ValueError):
        @architecture
        class MyArchitecture(Architecture):
            module = MyModule
            sig = Signal("sig", std_logic)
            sig1 = Signal("sig", std_logic)

    @architecture
    class MyArchitecture(Architecture):
        module = MyModule
        sig = Signal("sig", std_logic)
        sig1 = Signal("sig1", std_logic)
        sig2 = Signal("sig2", std_logic_vector(0, 3))

    assert MyArchitecture.serialize() == 'architecture rtl of MyModule is\n\t' \
                                         'signal sig : std_logic;' \
                                         '\n\tsignal sig1 : std_logic;' \
                                         '\n\tsignal sig2 : std_logic_vector (3 downto 0);' \
                                         '\nbegin\n' \
                                         'end architecture rtl;'

    @architecture
    class MyArchitecture(Architecture):
        module = MyModule
        sig = Signal("sig", std_logic)
        sig1 = Signal("sig1", std_logic)
        sig2 = Signal("sig2", std_logic_vector(0, 3))
        signalArray = [Signal("sig3", std_logic), Signal("sig4", std_logic)]


def test_procedure():
    @module
    class MyModule(Module):
        interfaces = None

    @architecture
    class MyArchitecture(Architecture):
        module = MyModule
        sig1 = Signal("sig", std_logic)

    @Process(MyArchitecture)
    class MyProcess(Process):
        name = "Pro"
        sensitivity = [MyArchitecture.sig1]
        pass

    @Process
    def myProcess():
        print("x")