import pytest
from pyhdl2 import *


def test_create_entity():
    @entity
    class MyEntity(Entity):
        name = "MyEntityName"
        interfaces = None

    @entity
    class MyEntityName(Entity):
        interfaces = None

    assert MyEntity.name == MyEntityName.name

    @entity
    class MyEntity(Entity):
        interfaces = None

    assert MyEntity.serialize() == "entity MyEntity is\n\t port ();\nend entity MyEntity;"


def test_entities_negative():
    with pytest.raises(TypeError):
        @entity
        class MyEntity(Entity):
            name = None
            interfaces = None

    with pytest.raises(TypeError):
        @entity
        class MyEntity(Entity):
            interfaces = 1

    with pytest.raises(AttributeError):
        @entity
        class MyEntity(Entity):
            name = "Name"
            pass

    with pytest.raises(TypeError):
        @entity
        class PoorlyDerivedEntity(int):
            interfaces = None

    with pytest.raises(TypeError):
        @entity
        class WrongSignalType(Entity):
            interfaces = ["NotAPortSignal"]


def test_create_architecture():
    @entity
    class MyEntity(Entity):
        interfaces = None

    @architecture
    class MyArchitecture(Architecture):
        entity = MyEntity
        sig = Signal("sig", std_logic)
        sig1 = Signal("sig1", std_logic)
        sig2 = Signal("sig2", std_logic_vector(0, 3))

    assert MyArchitecture.serialize() == 'architecture rtl of MyEntity is\n\t' \
                                         'signal sig : std_logic;' \
                                         '\n\tsignal sig1 : std_logic;' \
                                         '\n\tsignal sig2 : std_logic_vector (3 downto 0);' \
                                         '\nbegin\n' \
                                         'end architecture rtl;'

    @architecture
    class MyArchitecture(Architecture):
        entity = MyEntity
        sig = Signal("sig", std_logic)
        sig1 = Signal("sig1", std_logic)
        sig2 = Signal("sig2", std_logic_vector(0, 3))
        signalArray = [Signal("sig3", std_logic), Signal("sig4", std_logic)]


def test_architecture_negative():
    @entity
    class MyEntity(Entity):
        interfaces = None

    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            entity = None

    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            entity = MyEntity
            sig = PortSignal("sig", std_logic, Direction.In)

    with pytest.raises(TypeError):
        @architecture
        class MyArchitecture(Architecture):
            entity = MyEntity

        MyArchitecture.add_signal(1)

    with pytest.raises(ValueError):
        @architecture
        class MyArchitecture(Architecture):
            entity = MyEntity
            sig = Signal("sig", std_logic)
            sig1 = Signal("sig", std_logic)


def test_procedure_signal_next():
    with pytest.raises(ValueError):
        @entity
        class MyEntity(Entity):
            interfaces = [PortSignal("clk", std_logic, Direction.In)]

        @architecture
        class MyArchitecture(Architecture):
            entity = MyEntity

            sig = Signal("sig", std_logic)
            signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(2)]
            sig.next = std_logic(1)

            @process(sig)
            def my_process(self):
                self.sig.next = std_logic(1)
            pass


def test_procedure_signal_bad_type():
    with pytest.raises(TypeError):
        @entity
        class MyEntity(Entity):
            interfaces = [PortSignal("clk", std_logic, Direction.In)]

        @architecture
        class MyArchitecture(Architecture):
            entity = MyEntity

            sig = Signal("sig", std_logic)
            signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(2)]

            @process(sig)
            def my_process(self):
                self.sig.next = 1

    with pytest.raises(TypeError):
        @entity
        class MyEntity(Entity):
            interfaces = [PortSignal("clk", std_logic, Direction.In)]

        @architecture
        class MyArchitecture(Architecture):
            entity = MyEntity

            sig = Signal("sig", std_logic)
            signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(2)]

            @process(sig)
            def my_process(self):
                self.sig.next = std_logic_vector(0, 3)


def test_procedure():
    @entity
    class MyEntity(Entity):
        interfaces = [PortSignal("clk", std_logic, Direction.In)]

    @architecture
    class MyArchitecture(Architecture):
        entity = MyEntity

        sig = Signal("sig", std_logic)
        signalVectors = [Signal(f"sig{i}", std_logic, std_logic(i % 2)) for i in range(2)]

        @process(sig)
        def my_process(self):
            self.sig.next = std_logic('X')

        pass

        @process(signalVectors)
        def my_process2(self):
            self.sig.next = std_logic('X')

        pass

    assert MyArchitecture.serialize() == \
           "architecture rtl of MyEntity is" \
           "\n\tsignal sig : std_logic;" \
           "\n\tsignal sig0 : std_logic := '0';" \
           "\n\tsignal sig1 : std_logic := '1';" \
           "\nbegin\n\tmy_process: process (sig)" \
           "\n\tbegin " \
           "\n\t\tsig <= 'X';" \
           "\n\tend process;" \
           "\n\t\n\tmy_process2: process (sig0, sig1)" \
           "\n\tbegin " \
           "\n\t\tsig <= 'X';" \
           "\n\tend process;" \
           "\nend architecture rtl;"
