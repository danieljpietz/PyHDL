from abc import abstractmethod, ABCMeta


class _PHDLObj(metaclass=ABCMeta):
    """Abstract parent class for all PHDL types"""

    @abstractmethod
    def value(self):  # pragma: no cover
        pass
