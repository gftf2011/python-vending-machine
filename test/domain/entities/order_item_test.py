import pytest

from datetime import datetime

from src.domain.entities.product import ProductEntity
from src.domain.entities.order_item import OrderItemEntity

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' OR 'create_new' methods to create an instance of this class."):
        product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
        OrderItemEntity("f3331752-6c11-4578-adb7-331d703cb445", product, product.get_unit_price(), product.get_qty(), datetime.now())

def test_should_create():
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)
    sut = OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))
    assert sut.get_id().get_value() == "f3331752-6c11-4578-adb7-331d703cb445"
    assert sut.get_price() == product.get_unit_price()
    assert sut.get_qty() == product.get_qty()
    assert sut.get_product().get_id().get_value() == product.get_id().get_value()
    assert sut.get_created_at().timestamp() == 0