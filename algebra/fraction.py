from __future__ import annotations

from typing import Generic, TypeVar

R = TypeVar('R')


def gcd(*values):
    """Calculates the greatest common denominator of the values

    >>> gcd()
    0
    >>> gcd(2)
    2
    >>> gcd(5, 10)
    5
    >>> gcd(6,15,10)
    1
    """
    if not values:
        return 0
    if len(values) == 2:
        a, b = values
        while b:
            a, b = b, a % b
        return a
    g = values[0]
    for value in values[1:]:
        g = gcd(g, value)
    return g


def is_fraction(other) -> bool:
    """Checks if a value is a fraction (has a numerator and denominator)

    Integers are fractions (they all have denominator 1)
    >>> is_fraction(1)
    True

    Floats are not fractions
    >>> is_fraction(1.)
    False
    """
    return hasattr(other, 'numerator') and hasattr(other, 'denominator')


class Fraction(Generic[R]):
    """Generic fraction over a commutative ring R"""
    def __init__(self, numerator: R, denominator: R) -> None:
        self.numerator = numerator
        self.denominator = denominator

    def as_divmod(self) -> tuple[R, R]:
        """Calculates the divmod of the numerator and denominator

        >>> Fraction(5,4).as_divmod()
        (1, 1)
        """
        return divmod(self.numerator, self.denominator)

    def as_ratio(self) -> tuple[R, R]:
        """Gives the numerator and denominator as a tuple

        >>> Fraction(4, 3).as_ratio()
        (4, 3)
        """
        return (self.numerator, self.denominator)

    def simplify(self) -> Fraction[R]:
        """Simplifies the fraction

        >>> Fraction(16, 8).simplify()
        Fraction(2, 1)
        """
        g = gcd(self.numerator, self.denominator)
        if not g:
            return self  # No simplification necessary
        return Fraction(self.numerator//g, self.denominator//g)

    def __repr__(self) -> str:
        return f'Fraction({repr(self.numerator)}, {repr(self.denominator)})'

    def __str__(self) -> str:
        """Shows values as a fraction

        >>> str(Fraction(1,3))
        '1/3'
        """
        return f'{self.numerator}/{self.denominator}'

    def __abs__(self) -> Fraction[R]:
        """Gives the absolute value of the fraction

        >>> abs(Fraction(-1, -1))
        Fraction(1, 1)
        """
        return Fraction(abs(self.numerator), abs(self.denominator))

    def __pos__(self) -> Fraction[R]:
        return Fraction(+self.numerator, self.denominator)

    def __neg__(self) -> Fraction[R]:
        """ Reverses the sign of the numerator

        >>> -Fraction(1, 5)
        Fraction(-1, 5)
        """
        return Fraction(-self.numerator, self.denominator)

    def __add__(self, other) -> Fraction:
        try:
            if is_fraction(other):
                return Fraction(self.numerator * other.denominator
                                + other.numerator * self.denominator,
                                self.denominator * other.denominator)
            # Default to denominator of 1
            return Fraction(self.numeratror + other * self.denominator,
                            self.denominator)
        except ValueError:
            return NotImplemented

    def __radd__(self, other) -> Fraction:
        try:
            if is_fraction(other):
                return Fraction(other.numerator * self.denominator
                                + self.numerator * other.denominator,
                                other.denominator * self.denominator)
            # Default to denominator of 1
            return Fraction(other * self.denominator + self.numerator,
                            self.denominator)
        except ValueError:
            return NotImplemented

    def __sub__(self, other) -> Fraction:
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __invert__(self) -> Fraction[R]:
        return Fraction(self.denominator, self.numerator)

    def __mul__(self, other):
        try:
            if is_fraction(other):
                return Fraction(self.numerator * other.numerator,
                                self.denominator * other.denominator)
            # Default to denominator of 1
            return Fraction(self.numerator * other,
                            self.denominator)
        except ValueError:
            return NotImplemented

    def __rmul__(self, other):
        try:
            if is_fraction(other):
                return Fraction(other.numerator * self.numerator,
                                other.denominator * self.denominator)
            # Default to denominator of 1
            return Fraction(other * self.numerator,
                            self.denominator)
        except ValueError:
            return NotImplemented

    def __truediv__(self, other):
        return ~(~self * other)

    def __rtruediv__(self, other):
        return other * ~self

    def __eq__(self, other):
        """Fraction equality

        n1/d1 == n2/d2 if there exists c1, c2 not equal to 0 such that
        n1/d1 * c1 == n2/d2 * c2

        >>> Fraction(1, 1) == Fraction(5, 5)
        True
        >>> Fraction(1, 2) == Fraction(1, 3)
        False
        >>> Fraction(0, 10) == Fraction(0, 120)
        True
        >>> Fraction(0, 0) == Fraction(0, 0)
        True
        >>> Fraction(1, 0) == Fraction(5, 0)
        True
        >>> Fraction(0, 0) == Fraction(1, 0)
        False
        """
        if not is_fraction(other):
            if not self.denominator:
                return False
            return self.numerator == other * self.denominator
        # if b == 0, e*b == 0 == f*d and since f != 0, d == 0/f == 0
        # Same arguement works in reverse if d == 0, b must be 0
        if (not self.denominator) != (not other.denominator):
            return False
        # by the same arguement if a == 0, c == 0 and if c == 0, a == 0
        if (not self.numerator) != (not other.numerator):
            return False
        # By the previous two checks we have 3 cases:
        # 1. 0/0 == 0/0 which is true
        # 2. a != 0, c != 0, a/0 == c/0 which is also true
        # 3. b != 0, d != 0, a/b == c/d which is just rational numbers
        # We use the equality check for the rational numbers
        # which also returns True whenever both denominators are 0
        return (self.numerator * other.denominator ==
                other.numerator * self.denominator)

    def __hash__(self):
        return hash(self.simplify().as_ratio())
