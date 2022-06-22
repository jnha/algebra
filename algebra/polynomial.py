from __future__ import annotations

from itertools import zip_longest
from typing import Generic, TypeVar

R = TypeVar('R')  # Type of coefficients
E = TypeVar('E')  # Type of exponents


class Polynomial(Generic[R, E]):
    """Generic Polynomials

    Implimented as a map from exponents to coefficients.
    Allows multivariate polynomials via direct products of exponents,
    and non integer coefficients as long as __add__ and __sub__ are implimented
    """
    pass  # This is more complicated, impliment later


class Univariate(Generic[R]):
    """Univariate polynomials with integer exponents

    implimented as a tuple
    """
    def __init__(self, *coefficients: R) -> None:
        end = next((len(coefficients)-i
                    for i, c in enumerate(reversed(coefficients)) if c),
                   -1)
        self.coeffs = coefficients[:end]

    def degree(self) -> int:
        """Return the degree of the polynomial

        >>> Univariate(1, 0, 1).degree()
        2
        """
        return len(self)-1

    # -- String representations --
    def __repr__(self):
        return 'Univariate('+', '.join(repr(c) for c in self)+')'

    def __str__(self):
        if not self:
            return '0'
        return '-' if self[-1] < 0 else '' + ''.join(reversed(
            ' - ' if c < 0 else ' + '
            + str(abs(c)) if abs(c) != 1 else ''
            + '' if i == 0 else 'x' if i == 1 else f'x**{i}'
            for i, c in enumerate(self) if c)[3:]
        )

    # -- Equality --
    def __eq__(self, other):
        """
        >>> Univariate(1, 2, 3) == Univariate(1, 2, 3)
        True
        >>> Univariate(1, 2, 4) == (1, 2, 4)
        True
        """
        return self.coeffs == other

    def __hash__(self):
        return hash(self.coeffs)

    # -- Container dunders --
    def __len__(self) -> int:
        return len(self.coeffs)

    def __getitem__(self, key) -> R:
        if isinstance(key, int) and key > len(self):
            return 0
        return self.coeffs[key]

    def __iter__(self):
        return iter(self.coeffs)

    def __reversed__(self):
        """
        >>> list(reversed(Univariate(1, 2, 3)))
        [3, 2, 1]
        """
        return reversed(self.coeffs)

    # -- Arithmetic operations --
    def __neg__(self) -> Univariate[R]:
        return Univariate(*(-x for x in self))

    def __add__(self, other) -> Univariate[R]:
        return Univariate(*(s+o for s, o
                          in zip_longest(self, other, fillvalue=0)))

    def __radd__(self, other) -> Univariate[R]:
        return self + other

    def __mul__(self, other) -> Univariate[R]:
        out = [0] * (len(self) + len(other))
        for i, s in self:
            for j, o in other:
                out[i+j] += s*o
        return Univariate(*out)

    def __rmul__(self, other) -> Univariate[R]:
        out = [0] * (len(self) + len(other))
        for i, s in self:
            for j, o in other:
                out[i+j] += o*s
        return Univariate(*out)

    def __lshift__(self, i):
        return Univariate(*(0,)*i, *self)

    def __rshift__(self, i):
        return Univariate(*self[i:])
