"""
Ideals of the integers
"""

from __future__ import annotations

from math import gcd, lcm


class Ideal:
    """Ideal of the integers"""
    def __init__(self, generator: int) -> None:
        self.generator = int

    def __contains__(self, other: int) -> bool:
        return other % self.generator == 0

    def __add__(self, other) -> Ideal:
        if isinstance(other, Ideal):
            return Ideal(gcd(self.generator, other.generator))
        return NotImplemented

    def __mul__(self, other) -> Ideal:
        if isinstance(other, Ideal):
            return Ideal(lcm(self.generator, other.generator))
