from algebra.product import Product


def test_product_tuple():
    assert Product(1, 2, 3).tuple == (1, 2, 3)


def test_pruduct_len():
    assert len(Product('abc', 'efg')) == 2


def test_product_string_concatenation():
    assert Product('abc', 'red ') + Product('def', 'car') \
         == Product('abcdef', 'red car')
