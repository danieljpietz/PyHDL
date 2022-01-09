from typing import Union
from os import PathLike, system
from datetime import datetime
from .meta import __version__
from .entity import Entity
from .architecture import Architecture
from .module import Module
from py_mini_racer import MiniRacer
import pkgutil


def preamble():
    return f"-- Generated using {__package__} version {__version__}" \
           f" on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} \n"


def libraries(architecture):
    nl = '\n'
    return f'{nl}'.join([f"library {key};\n"
                         f"{(f'{nl}'.join([f'use {key}.{package};' for package in architecture.libraries[key]]))}"
                         for key in architecture.libraries.keys()]).replace('library work;\n', '')


def beautify(input: str):
    script = pkgutil.get_data(__name__, "beautifier/beautify.js").decode("utf-8")
    script += f"f({input.__repr__()});"
    return MiniRacer().eval(script)


class Project:

    def __init__(self, entity: Union[Entity, Module], architecture: Architecture = None,
                 filepath: Union[Union[str, bytes, PathLike[str], PathLike[bytes]], None] = None):
        if architecture is None:
            architecture = entity
            entity = architecture.entity
        if architecture.entity != entity:
            raise ValueError("Mismatched Entity Architecture Pair")
        self.entity = entity
        self.architecture = architecture
        self.filepath = filepath

    def value(self, _beautify=True):
        _value = f"{preamble()}\n{libraries(self.architecture)}\n\n{self.entity.value()}\n\n{self.architecture.value()}"
        if _beautify:
            return beautify(_value)
        else:
            return _value

    def write_packages(self):
        for package in self.architecture.packages:
            with open(f"{package.name}.vhdl", 'w') as f:
                f.write(beautify(package.value()))
        return [f"{package.name}.vhdl" for package in self.architecture.packages]

    def write_out(self, filepath: Union[str, bytes, PathLike[str], PathLike[bytes], None] = None):
        if self.filepath != filepath:
            if filepath is not None:
                raise ValueError("Filepath mismatch.")
        else:
            if filepath is not None:
                self.filepath = filepath
            else:
                raise ValueError("No filepath")

        package_files = self.write_packages()

        with open(self.filepath, 'w') as f:
            f.write(self.value())
        project_files = package_files
        project_files.append(self.filepath)
        inspect(' '.join(project_files))


def inspect(files):
    print(f"ghdl -s {files}")
    system(f"ghdl -s {files}")


def write_out(filepath: Union[str, bytes, PathLike[str], PathLike[bytes]], entity: Union[Entity, Module],
              architecture: Architecture = None):
    if isinstance(entity, Module):
        architecture = entity
        entity = entity.entity
    Project(entity, architecture, filepath=filepath).write_out()
