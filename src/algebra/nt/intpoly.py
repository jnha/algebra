"""
Univariate polynomials over the integers
"""
from __future__ import annotations

from itertools import zip_longest


class IntPoly:
    """Univariate polynomials with integer coefficients

    implimented as a tuple
    """
    def __init__(self, *coefficients: int) -> None:
        end = next((len(coefficients)-i
                    for i, c in enumerate(reversed(coefficients)) if c),
                   -1)
        self.coeffs = coefficients[:end]

    def degree(self) -> int:
        """Return the degree of the polynomial

        >>> IntPoly(1, 0, 1).degree()
        2
        """
        return len(self)-1

    # -- String representations --
    def __repr__(self):
        return 'IntPoly('+', '.join(repr(c) for c in self)+')'

    def __str__(self):
        if not self:
            return '0'
        return '-' if self[-1] < 0 else '' + ''.join(reversed(
            ' - ' if c < 0 else ' + '
            + str(abs(c)) if abs(c) != 1 else ''
            + '' if i == 0 else 'x' if i == 1 else f'x**{i}'
            for i, c in enumerate(self) if c)[3:]
        )

    # -- Order --
    def __lt__(self, other):
        return self.coeffs[::-1] < other.coeffs

    def __le__(self, other):
        return self.coeffs[::-1] <= other.coeffs

    def __eq__(self, other):
        return self.coeffs == other.coeffs

    def __ne__(self, other):
        return self.coeffs != other.coeffs

    def __gt__(self, other):
        return self.coeffs[::-1] > other.coeffs

    def __ge__(self, other):
        return self.coeffs[::-1] >= other.coeffs

    def __hash__(self):
        return hash(self.coeffs)

    # -- Container dunders --
    def __len__(self) -> int:
        return len(self.coeffs)

    def __getitem__(self, key) -> int:
        return self.coeffs[key]

    def __iter__(self):
        return iter(self.coeffs)

    def __reversed__(self):
        """
        >>> list(reversed(IntPoly(1, 2, 3)))
        [3, 2, 1]
        """
        return reversed(self.coeffs)

    # -- Arithmetic operations --
    def __neg__(self) -> IntPoly:
        return IntPoly(*(-x for x in self))

    def __add__(self, other) -> IntPoly:
        return IntPoly(*(s+o for s, o
                         in zip_longest(self, other, fillvalue=0)))

    def __radd__(self, other) -> IntPoly:
        return self + other

    def __mul__(self, other) -> IntPoly:
        if not self:
            return self  # zero times zero is zero
        out = [0] * (len(self) + len(other))
        for i, s in self:
            for j, o in other:
                out[i+j] += s*o
        return IntPoly(*out)

    def __rmul__(self, other) -> IntPoly:
        return self * other

    def __lshift__(self, i):
        if not self:  # shifting 0 gives 0
            return self
        return IntPoly(*(0)*i, *self)

    def __rshift__(self, i):
        return IntPoly(*self[i:])


"""
def polygcd(a: IntPoly, b: IntPoly) -> list[IntPoly]:
    r = [a, b]
    d = len(a) - len(b)
    beta = -1 if d % 2 else 1
    psi = -1
    gamma = a[-1]
    while r[-1] != 0:
        psi = (gamma)**d//(psi**(d-1))
        d = len(r[-2]) - len(r[-1])
        beta = -gamma * psi**d
        gamma = r[-1][-1]
        r.append(rem(gamma**(d+1)*r[-2], r[-1]) // beta)
    return r
"""
