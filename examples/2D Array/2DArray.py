from pyhdl2 import *


@module
class Array2DExample(Module):
    vector3 = Array("vector3", integer, (3, 0))
    matrix_3x3 = Array("matrix_3x3", vector3, (3, 0))
    matrix_3x2 = Array("matrix_3x2", vector3, (2, 0))
    tensor_3x2x3 = Array("tensor_3x2x3", matrix_3x2, (3,0))

    sig1 = Signal("sig1", matrix_3x3)
    sig2 = Signal("sig2", matrix_3x3)
    tensor = Signal("tensor", tensor_3x2x3)
    sig3 = Signal("sig3", matrix_3x3)



    @concurrent
    def concurrent_statements(self):
        for i in range(3):
            for j in range(3):
                self.tensor[i][0][j].next = self.sig1[i][j]
                self.tensor[i][1][j].next = self.sig2[j][i]

        pass


write_out("array_2d.vhdl", Array2DExample)