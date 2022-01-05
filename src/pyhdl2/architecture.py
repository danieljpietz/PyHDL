from .core import _PHDLObj
from .entity import Entity
from .signal import _Signal, Signal, PortSignal
from typing import List, Dict, Tuple
from .check import check_name
from .process import Process
import itertools
from .type import generate_typestrings, isarray


class Architecture(_PHDLObj):
    entity: Entity
    signals: List[Signal] = []
    processes: List[Process] = []
    libraries: Dict[str, Tuple[str]] = {}
    types: List[type] = []
    typestrings: str
    name: str

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
        _signals = ";\n\t".join([f'signal {signal.serialize_declaration()}' for signal in self.signals]) + ';' \
            if len(self.signals) > 0 \
            else ""

        _processes = '\n\n'.join([process.value() for process in self.processes])
        _processes = '\t' + _processes.replace('\n', '\n\t')

        _typestrings = self.typestrings.replace('\n', '\n\t')
        _typestrings = f"\n\t{_typestrings}\n" if len(_typestrings) != 0 else ''

        return f"architecture rtl of {self.entity.name} is\n" \
               f"{_typestrings}" \
               f"\n\t{_signals}\n\n" \
               f"begin\n" \
               f"{_processes}\n" \
               f"end architecture rtl;"


def architecture(Target):
    if not issubclass(Target, Architecture):
        raise TypeError(f"Architecture {Target} must inherit Architecture")
    if not isinstance(Target.entity, Entity):
        raise TypeError(f"{Target.entity.__class__.__name__} object not derived from Entity")
    if not hasattr(Target, 'name'):
        Target.name = f"{Target.entity.name}_rtl"
    check_name(Target.name)

    Target.signals = []
    target_new_signals = []
    for member in Target.__dict__:
        sig = Target.__dict__[member]
        if isinstance(sig, Signal):
            target_new_signals.append(sig)
        elif isarray(sig) and member not in ['signals', 'name']:
            if len(sig) > 1 and isinstance(sig[0], Signal):
                for signal in sig:
                    target_new_signals.append(signal)
    for signal in target_new_signals:
        Target.add_signal(Target, signal)
    for signal in Target.entity.interfaces:
        setattr(Target, signal.name, signal)
    target = Target()
    get_architecture_processes(target)
    get_architecture_types(target)
    return target


def get_architecture_processes(target):
    _architecture = type(target)
    for item in _architecture.__dict__:
        if isinstance(_architecture.__dict__[item], Process):
            _architecture.__dict__[item].architecture = _architecture
            _architecture.__dict__[item].invoke()


def get_architecture_types(target):
    for signal in list(itertools.chain(*[target.signals, target.entity.interfaces])):
        if signal.type not in target.types:
            target.types.append(signal.type)

    custom_types = set()

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
        else:
            custom_types.add(_type)
    target.typestrings = generate_typestrings(custom_types)
