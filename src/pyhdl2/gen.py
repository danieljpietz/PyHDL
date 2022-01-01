from .pyhdl import Entity, Architecture
from .types import enforce_types
from typing import Optional, Union
from os import PathLike
from datetime import datetime
from .meta import __version__

def preamble():
    return f"-- Generated using {__package__} version {__version__}" \
           f" on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} \n"


def libraries():
    return f"library IEEE;\n" \
           f"use IEEE.std_logic_1164.all;"


@enforce_types
class Module:

    def __init__(self, entity: Entity, architecture: Architecture,
                 filepath: Optional[Optional[Union[Union[str, bytes, PathLike[str], PathLike[bytes]]]]]):
        if architecture.entity != entity:
            raise ValueError("Mismatched Entity Architecture Pair")
        self.entity = entity
        self.architecture = architecture
        self.filepath = filepath

    def serialize(self):
        return f"{preamble()}\n{libraries()}\n\n{self.entity.serialize()}\n\n{self.architecture.serialize()}"

    def writeout(self, filepath: Optional[Union[Union[str, bytes, PathLike[str], PathLike[bytes]]]] = None):
        if self.filepath != filepath:
            if filepath is not None:
                raise ValueError("Filepath mismatch.")
        else:
            if filepath is not None:
                self.filepath = filepath
            else:
                raise ValueError("No filepath")

        with open(self.filepath, 'w') as f:
            f.write(self.serialize())


def writeout(entity: Entity, architecture: Architecture,
             filepath: Union[Union[str, bytes, PathLike[str], PathLike[bytes]]]):
    Module(entity, architecture, filepath=filepath).writeout()