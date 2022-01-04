from typing import Optional, Union
from os import PathLike
from datetime import datetime
from .meta import __version__
from .entity import Entity
from .architecture import Architecture

def preamble():
    return f"-- Generated using {__package__} version {__version__}" \
           f" on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} \n"


def libraries(architecture):
    nl = '\n'
    return f'{nl}'.join([f"library {key};\n"
                         f"{(f'{nl}'.join([f'use {key}.{package};' for package in architecture.libraries[key]]))}"
                         for key in architecture.libraries.keys()])


class Module:

    def __init__(self, entity: Entity, architecture: Architecture,
                 filepath: Union[Union[str, bytes, PathLike[str], PathLike[bytes]]]):
        if architecture.entity != entity:
            raise ValueError("Mismatched Entity Architecture Pair")
        self.entity = entity
        self.architecture = architecture
        self.filepath = filepath

    def serialize(self):
        return f"{preamble()}\n{libraries(self.architecture)}\n\n{self.entity.value()}\n\n{self.architecture.value()}"

    def write_out(self, filepath: Union[str, bytes, PathLike[str], PathLike[bytes], None] = None):
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


def write_out(entity: Entity, architecture: Architecture,
             filepath: Union[str, bytes, PathLike[str], PathLike[bytes]]):
    Module(entity, architecture, filepath=filepath).write_out()
