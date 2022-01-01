from .types import _PHDLObj, Signal, PortSignal, enforce_types
from typing import List, Optional
from collections.abc import Iterable
from .process import Process


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
    return target
    pass


@enforce_types
class Architecture(_PHDLObj):
    entity: Entity
    signals: List[Signal] = []
    processes: List[Process] = []

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

        return f"architecture rtl of {self.entity.name} is\n" \
               f"\t{_signals}\n" \
               f"begin\n" \
               f"{_processes}\n" \
               f"end architecture rtl;"
