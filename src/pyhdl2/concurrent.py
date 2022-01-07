from .process import Process


class Concurrent(Process):

    def __init__(self, func):
        self.func = func
        super(Concurrent, self).__init__()

    def value(self):
        return self.proc_str


def concurrent(func):
    return Concurrent(func)