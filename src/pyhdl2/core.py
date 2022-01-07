from abc import abstractmethod, ABCMeta
import os
import pkgutil


class _PHDLObj(metaclass=ABCMeta):
    """Abstract parent class for all PHDL types"""

    @abstractmethod
    def value(self):  # pragma: no cover
        pass


def f_string_from_template(path, **kwargs):
    fString = pkgutil.get_data(__name__, os.path.join('VHDL', path)).decode("utf-8")
    return fString.format(**kwargs)


def indent(_str: str, level: int):
    return '\t' * level + _str.replace('\n', '\t'*level)