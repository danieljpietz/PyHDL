from pyhdl2 import *
import numpy as np


@module
class MatMul(Module):
    clk = PortSignal("clk", std_logic, Direction.In)
    matrix4x4 = Array("matrix", integer, (15, 0))
    input1 = PortSignal("input1", matrix4x4, Direction.In)
    input2 = PortSignal("input2", matrix4x4, Direction.In)
    output = PortSignal("output", matrix4x4, Direction.Out)

    @RISING_EDGE(clk)
    def behavior(self):
        input1_numpy = np.array(self.input1).reshape(4, 4)
        input2_numpy = np.array(self.input2).reshape(4, 4)
        output_numpy = (input1_numpy @ input2_numpy).flatten()
        for (out, out_np) in zip(self.output, output_numpy):
            out.next = out_np


write_out("MatMul.vhdl", MatMul)

