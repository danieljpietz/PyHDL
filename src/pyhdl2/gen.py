from .pyhdl import Entity, Architecture
from .types import enforce_types
from typing import Optional
from datetime import datetime


def preamble():
    from .__init__ import __version__
    return f"-- Generated using {__package__} version {__version__}" \
           f" on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} \n"


def libraries():
    return f"library IEEE;\n" \
           f"use IEEE.std_logic_1164.all;"


@enforce_types
class Module:

    def __init__(self, entity: Entity, architecture: Architecture, filepath: Optional[str] = None):
        if architecture.entity != entity:
            raise ValueError("Mismatched Entity Architecture Pair")
        self.entity = entity
        self.architecture = architecture
        self.filepath = filepath

    def serialize(self):
        return f"{preamble()}\n{libraries()}\n\n{self.entity.serialize()}\n\n{self.architecture.serialize()}"

    def writeout(self, filepath=None):
        if self.filepath != filepath:
            if filepath is not None:
                raise ValueError("Filepath mismatch.")
        else:
            if filepath is not None:
                self.filepath = filepath
            else:
                raise ValueError("No filepath")

        with open(self.filepath, "w") as f:
            f.write(self.serialize())


def writeout(entity: Entity, architecture: Architecture, filepath: str):
    Module(entity, architecture, filepath).writeout()