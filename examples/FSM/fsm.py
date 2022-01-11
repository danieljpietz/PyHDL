from pyhdl2 import *


@fsm
class FSMExample(FSM):
    input = PortSignal("input", std_logic, Direction.In)
    signal1 = Signal("signal1", std_logic_vector(0, 100))

    @state
    def state1(self):
        @IF(rising_edge(self.clk))
        def my_if():
            for sig in self.signal1:
                sig.next = std_logic(1)
            pass




write_out("FSMExample.vhdl", FSMExample)
