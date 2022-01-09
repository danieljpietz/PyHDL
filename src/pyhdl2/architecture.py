from .core import _PHDLObj, f_string_from_template, indent
from .entity import Entity
from .signal import Signal, PortSignal
from typing import List, Dict
from .check import check_name
from .process import Process
import itertools
from .type import generate_typestrings, get_subtypes_from_list
from .concurrent import Concurrent

class Architecture(_PHDLObj):

    def __init__(self):
        self.signals: List[Signal] = []
        self.statements: List[Process] = []
        self.libraries: Dict[str, List[str]] = {}
        self.types: List[type] = []
        self.packages = set()
        self.components = []
        pass

    def add_signal(self, sig):
        if isinstance(sig, PortSignal):
            raise TypeError(f"{sig.__class__.__name__} object cannot be derived from PortSignal")
        elif isinstance(sig, Signal):
            for signal in self.signals:
                if signal.name == sig.name:
                    raise ValueError("Found duplicate signal {}".format(signal.name))
            if not hasattr(self, sig.name):
                self.__setattr__(sig.name, sig)
            self.signals.append(sig)
        else:
            raise TypeError(f"{sig.__class__.__name__} object not derived from Signal")

    def value(self):
        _signals = '\t' + self.signals_string()

        functionality = '\n\n'.join([statement.value() for statement in self.statements])
        functionality = indent(functionality, 1)

        types = indent(self.typestrings, 1)
        types = f"\n\t{types}\n" if len(types) != 0 else ''

        components = '\n'.join([comp.value() for comp in self.get_components()])

        declarations = types + _signals + components
        return f_string_from_template("architecture.vhdl",
                                      name=self.name,
                                      entity=self.entity.name,
                                      declarations=declarations,
                                      functionality=functionality)

    def get_components(self):
        from .component import Component
        return filter(lambda elem: isinstance(elem, Component), type(self).__dict__.values())
        pass

    def get_signals(self):
        return self.signals + list(self.entity.interfaces)

    def signals_string(self):
        return ";\n\t".join([f'{signal.serialize_declaration()}' for signal in self.signals]) + ';' \
            if len(self.signals) > 0 \
            else ""

    def add_element_libs_and_packs(self, elem):
        for key in elem.requires.keys():
            if key in self.libraries:
                for key_new in elem.requires[key]:
                    if key_new not in self.libraries[key]:
                        self.libraries[key].append(key_new)

            else:
                self.libraries[key] = set([k for k in elem.requires[key]]) \
                    if isinstance(elem.requires[key], (list, tuple)) else [elem.requires[key]]
                if hasattr(elem, 'package'):
                    self.packages.add(elem.package)


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

    get_architecture_types(target)
    get_architecture_processes(target)
    return target


def get_signals_recursive(items):
    _items = []
    for item in items:
        if isinstance(item, Signal):
            _items.append(item)
        elif isinstance(item, List) and not isinstance(item, str):
            _items += get_signals_recursive(item)
    return _items


def _architecture(target):
    target.signals = []
    target_new_signals = get_signals_recursive(type(target).__dict__.values())
    for signal in target_new_signals:
        target.add_signal(signal)

    for signal in target.entity.interfaces:
        setattr(target, signal.name, signal)


def get_architecture_processes(_architecture):
    for p in type(_architecture).__dict__.values():
        if isinstance(p, Process) or isinstance(p, Concurrent):
            p.set_signals(_architecture.get_signals())
            p.set_types(_architecture.types)
            p.set_components(list(_architecture.get_components()))
            p.set_architecture(_architecture)
            _architecture.statements.append(p)


def get_architecture_types(target):
    target.types = get_subtypes_from_list(
        [signal.type for signal in list(itertools.chain(*[target.signals, target.entity.interfaces]))])

    custom_types = []

    for _type in target.types:
        if _type.requires is not None:
            target.add_element_libs_and_packs(_type)
        else:
            custom_types.append(_type)
    target.typestrings = generate_typestrings(custom_types)

