from algebra.nt.intpoly import IntPoly, polygcd


# -- polygcd --
def test_polygcd_zero():
    assert polygcd(IntPoly(0), IntPoly(5)) == IntPoly(5)
    assert polygcd(IntPoly(5), IntPoly(0)) == IntPoly(5)


def test_polygcd_int():
    assert polygcd(IntPoly(10), IntPoly(5)) == IntPoly(5)
    assert polygcd(IntPoly(5), IntPoly(3)) == IntPoly(1)