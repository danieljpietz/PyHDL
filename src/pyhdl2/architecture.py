from .core import _PHDLObj, f_string_from_template, indent
from .entity import Entity
from .signal import Signal, PortSignal
from typing import List, Dict, Tuple
from .check import check_name
from .process import Process
import itertools
from .type import generate_typestrings, get_subtypes_from_list


class Architecture(_PHDLObj):

    def __init__(self):
        self.signals: List[Signal] = []
        self.processes: List[Process] = []
        self.libraries: Dict[str, Tuple[str]] = {}
        self.types: List[type] = []
        self.packages = set()
        pass

    def add_signal(self, sig):
        if isinstance(sig, PortSignal):
            raise TypeError(f"{sig.__class__.__name__} object cannot be derived from PortSignal")
        elif isinstance(sig, Signal):
            for signal in self.signals:
                if signal.name == sig.name:
                    raise ValueError("Found duplicate signal {}".format(signal.name))
            self.signals.append(sig)
        else:
            raise TypeError(f"{sig.__class__.__name__} object not derived from Signal")

    def value(self):
        _signals = '\t' + self.signals_string()

        functionality = '\n\n'.join([process.value() for process in self.processes])
        functionality = indent(functionality, 1)

        types = indent(self.typestrings, 1)
        types = f"\n\t{types}\n" if len(types) != 0 else ''

        declarations = _signals + types

        return f_string_from_template("architecture.vhdl",
                                      name=self.name,
                                      entity=self.entity.name,
                                      declarations=declarations,
                                      functionality=functionality)

    def signals_string(self):
        return ";\n\t".join([f'{signal.serialize_declaration()}' for signal in self.signals]) + ';' \
            if len(self.signals) > 0 \
            else ""


def architecture(Target):
    target = Target()
    if not issubclass(Target, Architecture):
        raise TypeError(f"Architecture {Target} must inherit Architecture")
    if not isinstance(Target.entity, Entity):
        raise TypeError(f"{Target.entity.__class__.__name__} object not derived from Entity")
    if not hasattr(Target, 'name'):
        target.name = f"{target.entity.name}_rtl"
    check_name(target.name)

    _architecture(target)

    get_architecture_processes(target)
    get_architecture_types(target)
    return target


def _architecture(target):
    target.signals = []
    target_new_signals = []
    for sig in type(target).__dict__.values():
        if isinstance(sig, Signal):
            target_new_signals.append(sig)
    # target_new_signals = get_signals_from_list(target_new_signals)
    for signal in target_new_signals:
        target.add_signal(signal)

    for signal in target.entity.interfaces:
        setattr(target, signal.name, signal)


def get_architecture_processes(_architecture):
    for p in type(_architecture).__dict__.values():
        if isinstance(p, Process):
            p.architecture = _architecture
            p.invoke()


def get_architecture_types(target):
    target.types = get_subtypes_from_list(
        [signal.type for signal in list(itertools.chain(*[target.signals, target.entity.interfaces]))])

    custom_types = []

    for _type in target.types:
        if _type.requires is not None:
            for key in _type.requires.keys():
                if key in target.libraries:
                    for key_new in _type.requires[key]:
                        if key_new not in target.libraries[key]:
                            target.libraries[key].add(key_new)

                else:
                    target.libraries[key] = set([k for k in _type.requires[key]]) \
                        if isinstance(_type.requires[key], (list, tuple)) else [_type.requires[key]]
                    if hasattr(_type, 'package'):
                        target.packages.add(_type.package)
        else:
            custom_types.append(_type)
    target.typestrings = generate_typestrings(custom_types)
