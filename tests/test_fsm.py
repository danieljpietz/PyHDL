from pyhdl2 import *


def test_create_fsm():

    @fsm
    class MyFSM(FSM):
        input = PortSignal("input", std_logic_vector(0, 8), Direction.In)
        output = PortSignal("output", std_logic_vector(0, 8), Direction.Out)

        testSignal = Signal("testSignal", std_logic)

        @state
        def state_1(self):
            self.testSignal.next = std_logic(1)
            self.output[4].next = self.input[3]
            pass

        @state
        def state_2(self):
            pass

