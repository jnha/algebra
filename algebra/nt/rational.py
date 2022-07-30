"""
Rational numbers
"""
from __future__ import annotations

from math import gcd


def is_rational(x):
    return isinstance(x, Rational) or isinstance(x, int)


class Rational:
    """Generic fraction over a commutative ring R"""
    def __init__(self, numerator: int, denominator: int) -> None:
        self.numerator = numerator
        self.denominator = denominator

    def as_divmod(self) -> tuple[int, int]:
        """Calculates the divmod of the numerator and denominator

        >>> Rational(5,4).as_divmod()
        (1, 1)
        """
        return divmod(self.numerator, self.denominator)

    def as_ratio(self) -> tuple[int, int]:
        """Gives the numerator and denominator as a tuple

        >>> Fraction(4, 3).as_ratio()
        (4, 3)
        """
        return (self.numerator, self.denominator)

    def simplify(self) -> Rational:
        """Simplifies the fraction

        >>> Fraction(16, 8).simplify()
        Fraction(2, 1)
        """
        g = gcd(self.numerator, self.denominator)
        if not g:
            return self  # No simplification necessary
        return Rational(self.numerator//g, self.denominator//g)

    def __repr__(self) -> str:
        return f'Rational({repr(self.numerator)}, {repr(self.denominator)})'

    def __str__(self) -> str:
        """Shows values as a fraction

        >>> str(Rational(1,3))
        '1/3'
        """
        return f'{self.numerator}/{self.denominator}'

    def __abs__(self) -> Rational:
        """Gives the absolute value of the fraction

        >>> abs(Fraction(-1, -1))
        Fraction(1, 1)
        """
        return Rational(abs(self.numerator), abs(self.denominator))

    def __pos__(self) -> Rational:
        return Rational(+self.numerator, self.denominator)

    def __neg__(self) -> Rational:
        """ Reverses the sign of the numerator

        >>> -Fraction(1, 5)
        Fraction(-1, 5)
        """
        return Rational(-self.numerator, self.denominator)

    def __add__(self, other) -> Rational:
        if is_rational(other):
            return Rational(self.numerator * other.denominator
                            + other.numerator * self.denominator,
                            self.denominator * other.denominator)
        return NotImplemented

    def __radd__(self, other) -> Rational:
        return self + other

    def __sub__(self, other) -> Rational:
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __invert__(self) -> Rational:
        return Rational(self.denominator, self.numerator)

    def __mul__(self, other):
        if is_rational(other):
            return Rational(self.numerator * other.numerator,
                            self.denominator * other.denominator)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

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
        if not is_rational(other):
            return False
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
