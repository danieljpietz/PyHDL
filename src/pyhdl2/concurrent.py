from .statements import Statements


class Concurrent(Statements):

    def __init__(self, func):
        self.set_function(func)

    def value(self):
        return super(Concurrent, self).value()


def concurrent(func):
    return Concurrent(func)