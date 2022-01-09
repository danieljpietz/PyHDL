from pyhdl2 import *


@fsm
class FSMExample(FSM):
    input = PortSignal("input", std_logic, Direction.In)

    @state
    def state1(self):
        @IF(self.input == std_logic('1'))
        def state1_if():
            self.state.next = self.states('state1')

            @ELSE()
            def state1_else():
                self.state.next = self.states('state2')

        pass

    @state
    def state2(self):
        @IF(self.input == std_logic('1'))
        def state2_if():
            self.state.next = self.states('state2')

            @ELSE()
            def state2_else():
                self.state.next = self.states('state1')
            pass

    @state
    def state3(self):
        pass


write_out("FSMExample.vhdl", FSMExample)
