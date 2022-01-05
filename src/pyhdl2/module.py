from typing import Union
from os import PathLike
from datetime import datetime
from .meta import __version__
from .entity import Entity
from .architecture import Architecture
from py_mini_racer import MiniRacer
import pkgutil


def preamble():
    return f"-- Generated using {__package__} version {__version__}" \
           f" on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} \n"


def libraries(architecture):
    nl = '\n'
    return f'{nl}'.join([f"library {key};\n"
                         f"{(f'{nl}'.join([f'use {key}.{package};' for package in architecture.libraries[key]]))}"
                         for key in architecture.libraries.keys()])


def beautify(input: str):
    script = pkgutil.get_data(__name__, "beautifier/beautify.js").decode("utf-8")
    script += f"f({input.__repr__()});"
    return MiniRacer().eval(script)


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

        raw = self.serialize()

        try:
            pretty = beautify(raw)
            with open(self.filepath, 'w') as f:
                f.write(pretty)
        except:
            print("Beautify Failed")
            with open(self.filepath, 'w') as f:
                f.write(raw)


def write_out(entity: Entity, architecture: Architecture,
              filepath: Union[str, bytes, PathLike[str], PathLike[bytes]]):
    Module(entity, architecture, filepath=filepath).write_out()
