import pytest
from pyhdl2 import *



def test_statements():

    sig1 = Signal("sig1", std_logic)
    sig2 = Signal("sig2", std_logic)

    def statementFunc(self):
        self.sig1.next = self.sig2

        def statement2Func(self):
            self.sig2.next = std_logic('1')

        statements2 = Statements([self.sig1, self.sig2], statement2Func)

        pass

    statements = Statements([sig1, sig2], statementFunc)
    statements.value()
    pass