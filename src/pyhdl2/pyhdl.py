from .types import _PHDLObj, Signal, PortSignal, enforce_types, Array
from typing import List, Optional, Dict
from collections.abc import Iterable
from .process import Process
import itertools


@enforce_types
class Entity(_PHDLObj):
    """Top Level Entity for an HDL design"""

    name: Optional[str]
    interfaces: Optional[List[PortSignal]]

    def serialize(self):
        nl = '\n\t\t   '

        _interfaces = \
            f"{f';{nl}'.join([f'{signal.name} : {signal.direction} {signal.type.serialize(signal.type)}' for signal in self.interfaces])}" \
                if self.interfaces is not None and isinstance(self.interfaces, Iterable) \
                else ""

        return f"entity {self.name} is\n" \
               f"\t port ({_interfaces});\n" \
               f"end entity {self.name};"


def entity(Target):
    if not isinstance(Target, type(Entity)):
        raise TypeError(
            'Unexpected type for \'{}\' (expected {} but found {})'.format(Target.__name__, Entity, type(Target)))
    target = Target()
    if not hasattr(target, 'name'):
        target.name = Target.__name__
    if not isinstance(target.name, str):
        raise TypeError(f"{target.name.__class__.__name__} object not of type \'str\'")
    if target.interfaces is not None and isinstance(target.interfaces, Iterable):
        for signal in target.interfaces:
            if not isinstance(signal, PortSignal):
                raise TypeError(f"{signal.__class__.__name__} object not derived from PortSignal")
    elif target.interfaces is not None and not isinstance(target.interfaces, Iterable):
        raise TypeError(f"{target.interfaces.__class__.__name__} must be Iterable or None")
    for signal in target.interfaces:
        setattr(target, signal.name, signal)
    return target


def get_architecture_processes(target):
    architecture = type(target)
    for item in architecture.__dict__:
        if isinstance(architecture.__dict__[item], Process):
            architecture.__dict__[item].architecture = architecture
            architecture.__dict__[item].invoke()
    pass


def get_architecture_types(target):
    for signal in list(itertools.chain(*[target.signals, target.entity.interfaces])):
        if signal.type not in target.types:
            target.types.append(signal.type)

    customTypes = set()

    for type in target.types:
        if type.requires is not None:
            for key in type.requires.keys():
                if key in target.libraries:
                    for newkey in type.requires[key]:
                        if newkey not in target.libraries[key]:
                            target.libraries[key].add(newkey)
                else:
                    target.libraries[key] = set([k for k in type.requires[key]]) \
                        if isinstance(type.requires[key], (list, tuple)) else [type.requires[key]]
        else:
            customTypes.add(type)
    target.typestrings = generate_typestrings(customTypes)


def generate_typestrings(types):
    for outer_custom_type in types:
        for inner_custom_type in types:
            if inner_custom_type is outer_custom_type:
                break
            elif inner_custom_type.name == outer_custom_type.name:
                if generate_typestring(inner_custom_type) != generate_typestring(outer_custom_type):
                    raise ValueError (f"Found multiple definitions for type {inner_custom_type.name}.")
    return '\n'.join(set([generate_typestring(custom_type) for custom_type in types]))
    pass


def generate_typestring(custom_type):
    return f"type {custom_type.name} is array of {custom_type.type.__name__} ({max(custom_type.bounds)} " \
           f"downto {min(custom_type.bounds)});" if issubclass(custom_type, Array) else ''


def architecture(Target):
    if not isinstance(Target.entity, Entity):
        raise TypeError(f"{Target.entity.__class__.__name__} object not derived from Entity")
    Target.signals = []
    target_new_signals = []
    for member in Target.__dict__:
        if isinstance(Target.__dict__[member], Signal):
            target_new_signals.append(Target.__dict__[member])
        elif isinstance(Target.__dict__[member], Iterable) and member != 'signals':
            if len(Target.__dict__[member]) > 1 and isinstance(Target.__dict__[member][0], Signal):
                for signal in Target.__dict__[member]:
                    target_new_signals.append(signal)
    for signal in target_new_signals:
        Target.add_signal(Target, signal)
    for signal in Target.entity.interfaces:
        setattr(Target, signal.name, signal)
    target = Target()
    get_architecture_processes(target)
    get_architecture_types(target)
    return target
    pass


@enforce_types
class Architecture(_PHDLObj):
    entity: Entity
    signals: List[Signal] = []
    processes: List[Process] = []
    libraries: Dict = {}
    types: List = []

    def add_signal(self, sig):
        if isinstance(sig, Signal) and not isinstance(sig, PortSignal):
            for signal in self.signals:
                if signal.name == sig.name:
                    raise ValueError("Found duplicate signal {}".format(signal.name))
            """if not hasattr(self, sig.name):
                setattr(self, sig.name, sig)"""
            self.signals.append(sig)
        elif isinstance(sig, PortSignal):
            raise TypeError(f"{sig.__class__.__name__} object cannot be derived from PortSignal")
        else:
            raise TypeError(f"{sig.__class__.__name__} object not derived from Signal")

    def serialize(self):
        _signals = ";\n\t".join([f'signal {signal.serialize()}' for signal in self.signals]) + ';' \
            if len(self.signals) > 1 \
            else f"signal {self.signals[0]};" if len(self.signals) == 1 \
            else ""

        _processes = '\n\n'.join([process.serialize() for process in self.processes])
        _processes = '\t' + _processes.replace('\n', '\n\t')

        _typestrings = self.typestrings.replace('\n', '\n\t')

        return f"architecture rtl of {self.entity.name} is\n" \
               f"\n\t{_typestrings}\n\n" \
               f"\t{_signals}\n\n" \
               f"begin\n" \
               f"{_processes}\n" \
               f"end architecture rtl;"
