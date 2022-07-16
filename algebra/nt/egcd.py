from __future__ import annotations

import timeit


def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm

    Uses the standard euclidean algorithm to calculate the greatest common
    divisor d of a and b along with x, y such that ax + by = d

    Returns d, x, y"""
    # We want d, x, y such that ax + by = d
    # using the invariants:
    # a u1 + b u2 = u
    # a v1 + b v2 = v
    u, u1, u2 = a, 1, 0
    v, v1, v2 = b, 0, 1
    while v != 0:
        q, r = divmod(u, v)
        # We already know v = a*v1 + b*v2
        # but we need r = a(?) + b(?)
        # u = qv + r <=> r = u - qv
        # r = (a*u1 + b*u2) - q(a*v1 + b*v2)
        # = a(u1 - q*v1) - b(u2 - q*v2)
        (u, u1, u2), (v, v1, v2) = (v, v1, v2), (r, u1-q*v1, u2-q*v2)
    # We didn't bother calculating u2, v2
    # recover from a*u1 + b*u2 = u <=> u2 = (u - a*u1)/b
    return u, u1, u2


# GCD implimentation varients
def _rgcd(a: int, b: int) -> int:
    """Recursive Euclid gcd"""
    if b == 0:
        return a
    return _rgcd(b, a % b)


def _regcd(a: int, b: int) -> tuple[int, int, int]:
    """Recursive Euclid egcd"""
    if b == 0:
        return a, 1, 0
    q, r = divmod(a, b)
    d, x, y = _regcd(b, r)
    # a = qb + r <=> r = a - qb
    # d = bx + ry = bx + (a - qb)y = bx + ay -qby
    #   = ay + b(x - qy)
    return d, y, x - q*y


def _igcd(a: int, b: int) -> int:
    """Iterative Euclid gcd"""
    while b != 0:
        a, b = b, a % b
    return a


def _iegcd(a: int, b: int) -> int:
    """Iterative Euclide egcd"""
    # Invariants:
    # a u1 + b u2 = u
    # a v1 + b v2 = v
    u, u1, u2 = a, 1, 0
    v, v1, v2 = b, 0, 1
    while v != 0:
        q, r = divmod(u, v)
        # We already know v = a*v1 + b*v2
        # but we need r = a(?) + b(?)
        # u = qv + r <=> r = u - qv
        # r = (a*u1 + b*u2) - q(a*v1 + b*v2)
        # = a(u1 - q*v1) - b(u2 - q*v2)
        (u, u1, u2), (v, v1, v2) = (v, v1, v2), (r, u1-q*v1, u2-q*v2)
    return u, u1, u2


def _iegcd2(a: int, b: int) -> int:
    """Iterative Euclide egcd, reconstruction version"""
    # We eliminate the variables u2, v2
    if b == 0:
        return a, 1, 0
    u, u1 = a, 1
    v, v1 = b, 0
    while v != 0:
        q, r = divmod(u, v)
        (u, u1), (v, v1) = (v, v1), (r, u1-q*v1)
    # Since a*u1 + b*u2 = u, u2 = (u - a*u1)/b
    return u, u1, (u-a*u1)/b


def v2(n: int):
    """2-adic valuation"""
    return (n & -n).bit_length() - 1


def _rbgcd(a: int, b: int) -> int:
    """Recursive binary gcd"""
    def helper(a: int, b: int) -> int:
        assert a % 2
        assert b % 2
        if a < b:
            a, b = b, a
        a, b = b, a-b
        if b == 0:
            return a
        return helper(a, b >> v2(b))
    if a == 0:
        return b
    if b == 0:
        return a
    sa, sb = v2(a), v2(b)
    a >>= sa
    b >>= sb
    return helper(a, b) << min(sa, sb)


def _ibgcd(a: int, b: int) -> int:
    """Iterative binary gcd"""
    if a == 0:
        return b
    if b == 0:
        return a
    sa, sb = v2(a), v2(b)
    a >>= sa
    b >>= sb
    while True:
        if a < b:
            a, b = b, a
        a -= b
        if a == 0:
            return b << min(sa, sb)
        a >>= v2(a)


# Performance of different implimentations
def gcd_benchmarks(gcd, extended=False):
    print(gcd.__doc__)

    def small_frac():
        for x in range(1000):
            for y in range(1000):
                d = gcd(x, y)
                not extended and d and (x//d, y//d)
    print('small simplification:', timeit.timeit(small_frac, number=1))
    print('progressively larger coprime gcds:')
    for n in range(1, 1000, 100):
        def cogcd():
            x, y = 2**n, 3**n
            d = gcd(x, y)
            not extended and d and (x//d, y//d)
        print(timeit.timeit(cogcd, number=1000))
    print('progressively larger non-coprime gcds:')
    for n in range(1, 1000, 100):
        def ncgcd():
            x, y = 6**n, 9**n
            d = gcd(x, y)
            not extended and d and (x//d, y//d)
        print(timeit.timeit(ncgcd, number=1000))


if __name__ == '__main__':
    """Conclusions from benchmarking:
    - builtin gcd is much faster than any python implimentation, as expected
    - recurive functions perform badly in python
    - egcd is slower than gcd + division to simplify fractions
    - _iegcd2 performs better than _iegcd but not significantly
    """
    from math import gcd
    gcd_benchmarks(gcd)
    print()
    gcd_benchmarks(_rgcd)
    print()
    gcd_benchmarks(_regcd, True)
    print()
    gcd_benchmarks(_igcd)
    print()
    gcd_benchmarks(_iegcd, True)
    print()
    gcd_benchmarks(_iegcd2, True)
    print()
    gcd_benchmarks(_rbgcd)
    print()
    gcd_benchmarks(_ibgcd)
