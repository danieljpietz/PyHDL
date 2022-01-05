from .core import _PHDLObj
from typing import Optional, Tuple
from .signal import PortSignal
from .check import check_name


class Entity(_PHDLObj):
    """Top Level Entity for an HDL design"""
    name: Optional[str]
    interfaces: Tuple[PortSignal]

    def interface_string(self):
        nl = '\n\t\t   '
        return f"{f';{nl}'.join([f'{signal.name} : {signal.direction} {signal.type.type_name}' for signal in self.interfaces])}" \
            if len(self.interfaces) > 0 else " "

    def value(self):
        return f"entity {self.name} is\n" \
               f"\t port ({self.interface_string()});\n" \
               f"end entity {self.name};"


def entity(Target):
    if not issubclass(Target, Entity):
        raise TypeError(
            'Unexpected type for \'{}\' (expected {} but found {})'.format(Target.__name__, Entity, type(Target)))
    target = Target()
    if not hasattr(target, 'name'):
        target.name = Target.__name__
    if not isinstance(target.name, str):
        raise TypeError(
            'Unexpected type for \'{}\' (expected {} but found {})'.format('entity name', str, type(target.name)))
    check_name(target.name)
    if isinstance(target.interfaces, tuple):
        for signal in target.interfaces:
            if not isinstance(signal, PortSignal):
                raise TypeError(
                    'Unexpected type for \'{}\' (expected {} but found {})'.format('signal', PortSignal, type(signal)))
    else:
        raise TypeError(
            'Unexpected type for \'{}\' (expected {} but found {})'.format('interface', tuple, type(target.interfaces)))
    for signal in target.interfaces:
        setattr(target, signal.name, signal)
    return target
