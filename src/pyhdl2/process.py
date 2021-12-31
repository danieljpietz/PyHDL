from dataclasses import dataclass
from .types import _PHDLObj, Signal
from typing import List, Optional
from collections.abc import Iterable


def process(argument):
    def decorator(function):
        print("0")
        def wrapper(*args, **kwargs):
            print("1")
            print(argument)
            result = function(*args, **kwargs)
            print("3")
            return result
        return wrapper
    return decorator


class Process(_PHDLObj):
    name: str
    sensitivity: Optional[List[Signal]] = None

    def __init__(self, architecture):
        self.architecture = architecture

    def serialize(self):
        _sensitivity = f"({', '.join([signal.name for signal in self.sensitivity])})" \
            if self.sensitivity is not None and isinstance(self.sensitivity, Iterable) \
            else ""

        _ser = f"{self.name}: process {_sensitivity}\n" \
               f"begin \n" \
               f"end process;"
        return _ser
