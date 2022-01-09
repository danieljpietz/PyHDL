from .module import Module
from .core import _PHDLObj, f_string_from_template
from .signal import PortSignal
from .statements import Statements
from .types import unconnected
from .check import check_name

class Component(_PHDLObj):

    def __init__(self, name: str, module: Module):
        self.module = module
        self.interfaces = list(filter(lambda x: isinstance(x, PortSignal), module.get_signals()))
        self.name = name
        check_name(name)
    def __call__(self, *args, **kwargs):
        for found, expected in zip(args, self.interfaces):
            if found.type != expected.type and found.type is not unconnected:
                raise TypeError(f"Unexpected type for {found.name}. "
                                f"Expected {expected.type.name}, found {found.type.name}")
        PortMap(self, args)

    def value(self):
        nl = '\n\t\t  '
        interfaces = f"{f';{nl}'.join([f'{signal.name} : {signal.direction} {signal.type.name}' for signal in self.interfaces])}" \
            if len(self.interfaces) > 0 else " "
        return f_string_from_template('component.vhdl',
                                      name=self.module.__class__.__name__,
                                      interfaces=interfaces)
        pass


port_map_count = -1


class PortMap(Statements):
    def __init__(self, comp: Component, args):
        self.comp = comp
        self.call_args = args
        super(PortMap, self).__init__(tuple(), None)

    def value(self):
        global port_map_count
        port_map_count += 1
        return f"{self.comp.name}{port_map_count}: {self.comp.module.__class__.__name__} port map" \
               f"({', '.join([f'{expected.name} => {actual.value(skip_direction_check=True)}' for expected, actual in zip(self.comp.interfaces, self.call_args)])});"
