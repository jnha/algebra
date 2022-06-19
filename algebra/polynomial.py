from __future__ import annotations

from itertools import zip_longest
from typing import Generic, TypeVar

R = TypeVar('R')


class Polynomial(Generic[R]):
    """Univariate polynomial"""
    def __init__(self, *coefficients: R) -> None:
        end = 1 + max((i for i, c in enumerate(coefficients) if c), default=-1)
        self.coeffs = coefficients[:end]

    def degree(self) -> int:
        """Return the degree of the polynomial

        >>> Polynomial(1, 0, 1).degree()
        2
        """
        return len(self)-1

    # -- Magic Methods --
    def __len__(self) -> int:
        return len(self.coeffs)

    def __getitem__(self, key) -> R:
        if isinstance(key, int) and key > len(self):
            return 0
        return self.coeffs[key]

    def __iter__(self):
        return iter(self.coeffs)

    def __reversed__(self):
        return reversed(self.coefficients)

    def __eq__(self, other):
        if not hasattr(other, 'coeffs'):
            return NotImplemented
        return self.coeffs == other.coeffs

    def __hash__(self):
        return hash(self.coeffs)

    def __repr__(self):
        if not self:
            return '0'
        return '-' if self[-1] < 0 else '' + ''.join(reversed(
            ' - ' if c < 0 else ' + '
            + str(abs(c)) if abs(c) != 1 else ''
            + '' if i == 0 else 'x' if i == 1 else f'x**{i}'
            for i, c in enumerate(self) if c)[3:]
        )

    def __neg__(self) -> Polynomial[R]:
        return Polynomial(*(-x for x in self))

    def __add__(self, other) -> Polynomial[R]:
        if not hasattr(other, 'coeffs'):
            return NotImplemented
        return Polynomial(*(s+o for s, o
                          in zip_longest(self, other, fillvalue=0)))

    def __mul__(self, other) -> Polynomial[R]:
        return NotImplemented
