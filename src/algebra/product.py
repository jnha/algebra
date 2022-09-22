from __future__ import annotations

from typing import GenericAlias, Iterable


class Product():
    """Direct Product type

    Product impliments the algebraic direct product.
    It attempts to define operations pointwise on its elements
    as much as possible.
    """
    __slots__ = 'tuple'

    def __init__(self, *things) -> None:
        self.tuple = things

    # -- Tuple Magic --
    def __contains__(self, item) -> bool:
        return item in self.tuple

    def __getitem__(self, key):
        return self.tuple[key]

    def __iter__(self) -> Iterable:
        return iter(self.tuple)

    def __len__(self) -> int:
        return len(self.tuple)

    def __repr__(self) -> str:
        return 'Product' + repr(self.tuple)

    def __reversed__(self) -> Iterable:
        return reversed(self.tuple)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.tuple == other.tuple

    def __hash__(self, other):
        return hash(self.tuple)

    # -- Pointwise Magic --
    def __bool__(self) -> bool:
        return any(self)

    def __neg__(self) -> Product:
        try:
            return Product(*(-e for e in self))
        except TypeError:
            return NotImplemented

    def __pos__(self) -> Product:
        try:
            return Product(*(+e for e in self))
        except TypeError:
            return NotImplemented

    def __abs__(self) -> Product:
        try:
            return Product(*(abs(e) for e in self))
        except TypeError:
            return NotImplemented

    def __invert__(self) -> Product:
        try:
            return Product(*(~e for e in self))
        except TypeError:
            return NotImplemented

    def __add__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s + o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __radd__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o + s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __sub__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s - o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rsub__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o - s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __mul__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s * o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rmul__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o * s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __matmul__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s @ o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o @ s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __truediv__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s / o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o / s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __floordiv__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s // o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rfloordiv__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o // s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __mod__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s % o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rmod__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o % s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __divmod__(self, other) -> tuple[Product, Product]:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            div, mod = zip(divmod(s, o) for s, o in zip(self, other))
            return Product(*div), Product(*mod)
        except TypeError:
            return NotImplemented

    def __rdivmod__(self, other) -> tuple[Product, Product]:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            div, mod = zip(divmod(o, s) for s, o in zip(self, other))
            return Product(*div), Product(*mod)
        except TypeError:
            return NotImplemented

    def __pow__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s ** o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rpow__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o ** s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __lshift__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s << o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rlshift__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o << s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rshift__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s >> o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rrshift__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o >> s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __and__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s & o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rand__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o & s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __or__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s | o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __ror__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o | s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __xor__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(s ^ o for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    def __rxor__(self, other) -> Product:
        if not hasattr(other, '__len__') or len(other) != len(self):
            return NotImplemented
        try:
            return Product(*(o ^ s for s, o in zip(self, other)))
        except TypeError:
            return NotImplemented

    # -- Pointwise Attribute Magic --
    def __getattr__(self, name):
        """Define undefined attributes pointwise on elements"""
        if len(self) == 0:
            return AttributeError

        attrs = [getattr(e, name) for e in self]
        if all(hasattr(attr, '__call__') for attr in attrs):
            def pointwise(*args, **kwargs):
                return Product(
                    attr(
                        *(arg[i] for arg in args),
                        **{key: value[i] for key, value in kwargs.items()}
                    )
                    for i, attr in enumerate(attrs)
                )
            return pointwise
        else:
            return Product(*attrs)

    # -- Type Magic --
    def __class_getitem__(cls, key):
        return GenericAlias(cls, key)
