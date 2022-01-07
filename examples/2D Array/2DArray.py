from pyhdl2 import *


@module
class Array2DExample(Module):
    column = Array("inner", std_logic, (3, 0))
    matrix = Array("outer", column, (3, 0))

    sig = Signal("sig", matrix)

    @process()
    def my_process(self):
        for col in self.sig:
            for item in col:
                item.next = std_logic(1)
        pass


write_out("array_2d.vhdl", Array2DExample)