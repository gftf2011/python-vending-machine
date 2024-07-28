import pytest

from src.domain.entities.product import ProductEntity
from src.domain.exceptions.invalid_products_qty import InvalidProductsQtyException
from src.domain.exceptions.invalid_products_price import InvalidProductsPriceException

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        ProductEntity("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)

def test_should_raise_exception_if_quantity_is_negative():
    qty = -1
    with pytest.raises(InvalidProductsQtyException, match="quantity of products can not be negative"):
        ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", qty, "00", 0)

def test_should_raise_exception_if_unit_price_is_negative():
    unit_price = -1
    with pytest.raises(InvalidProductsPriceException, match="price of products can not be negative"):
        ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", unit_price)

def test_should_get_id():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    assert sut.id.value == "b9651752-6c44-4578-bdb6-883d703cbff5"

def test_should_get_code():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    assert sut.code == "00"

def test_should_get_name():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    assert sut.name == "Hersheys"

def test_should_get_qty():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    assert sut.qty == 0

def test_should_get_unit_price():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    assert sut.unit_price == 0

def test_should_increase_qty():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    sut.increase_qty()
    assert sut.qty == 1

def test_should_reduce_qty():
    sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    sut.reduce_qty()
    assert sut.qty == 0

def test_raise_exception_when_product_quantity_is_0():
    with pytest.raises(InvalidProductsQtyException, match="quantity of products can not be negative"):
        sut = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
        sut.reduce_qty()
