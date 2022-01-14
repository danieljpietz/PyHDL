from pyhdl2 import *


@fsm
class FSMExample(FSM):

    @state
    def state1(self):
        pass

    @state
    def state2(self):
        pass

    @state
    def state3(self):
        pass




write_out("FSMExample.vhdl", FSMExample)
