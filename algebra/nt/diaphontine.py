from __future__ import annotations

from egcd import egcd
from typing import Optional


def solve_linear(a, b, c) -> Optional[tuple[int, int]]:
    """Solve the equation ax + by = c"""
    d, x, y = egcd(a, b)
    if c % d:
        return None
    s = c//d
    return (x*s, y*s)
