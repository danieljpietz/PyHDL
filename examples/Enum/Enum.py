from pyhdl2 import *

@module
class EnumExample(Module):
    EnumType = Enum("EnumType", ("Option1", "Option2", "Option3") )

    sig = Signal("sig", EnumType, EnumType("Option1"))

    @process()
    def my_process(self):
        @IF(self.sig == self.EnumType("Option1"))
        def state_check():
            self.sig.next = self.EnumType("Option2")
        pass


write_out("EnumExample.vhdl", EnumExample)