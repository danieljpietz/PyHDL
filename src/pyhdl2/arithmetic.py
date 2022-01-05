from .core import _PHDLObj
from typing import Type, List, Tuple, Any, Optional


class Operable(_PHDLObj):
    def __add__(self, other):
        return operator(self, other, '+')

    def __sub__(self, other):
        return operator(self, other, '-')

    def __mul__(self, other):
        return operator(self, other, '*')

    def __truediv__(self, other):
        return operator(self, other, '/')

    def __and__(self, other):
        return operator(self, other, 'and')

    def __or__(self, other):
        return operator(self, other, 'or')

    def __xor__(self, other):
        return operator(self, other, 'xor')

    def __ne__(self, other):
        return operator(self, other, '!=')

    def __eq__(self, other):
        return operator(self, other, '=')

    def __gt__(self, other):
        return operator(self, other, '>')

    def __lt__(self, other):
        return operator(self, other, '<')

    def __ge__(self, other):
        return operator(self, other, '>=')

    def __le__(self, other):
        return operator(self, other, '<=')

    def __neg__(self):
        return operator(self, None, '-')

    def neg(self):
        return operator(self, None, 'not ')


class ArithmeticStack(Operable):

    def __init__(self):
        self.stack: List[Tuple[Operable, str]] = []
        self.type: Type[Any]
        pass

    def add(self, signal, op):
        if len(self.stack) == 0:
            self.type = signal.type
        else:
            self.type = self.type.type_check(self.type, signal.type, op)
        self.stack.append((signal, op))
        pass

    def value(self):
        if not isinstance(self.stack[0][0], ArithmeticStack):
            _value = f'{self.stack[0][1]}{self.stack[0][0].value()}'
        else:
            _value = f'{self.stack[0][1]}({self.stack[0][0].value()})'
        for (operand, op) in self.stack[1:]:
            if not isinstance(operand, ArithmeticStack):
                _value = f"{_value} {op} {operand.value()}"
            else:
                _value = f"{_value} {op} ({operand.value()})"
        return _value


def operator(left: Operable, right: Optional[Operable], op: str):
    if right is not None:
        if isinstance(left, ArithmeticStack):
            left.add(right, op)
            return left
        else:
            stack = ArithmeticStack()
            stack.add(left, '')
            stack.add(right, op)
            return stack
    else:
        stack = ArithmeticStack()
        stack.add(left, op)
        return stack
