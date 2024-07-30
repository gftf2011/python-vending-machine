from datetime import datetime

import pytest

from src.domain.entities.product import ProductEntity
from src.domain.entities.order_item import OrderItemEntity

from src.domain.exceptions.invalid_order_item_product_qty import (
    InvalidOrderItemProductQtyException,
)


def test_should_raise_exception_by_using_constructor():
    """Function to test if the software component will raise an exception if calls the constructor"""
    with pytest.raises(
        Exception,
        match="Use the 'create' OR 'create_new' methods to create an instance of this class.",
    ):
        product: ProductEntity = ProductEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0
        )
        OrderItemEntity(
            "f3331752-6c11-4578-adb7-331d703cb445",
            product,
            product.unit_price,
            product.qty,
            datetime.now(),
        )


def test_should_raise_exception_if_product_is_out_of_stock():
    """Function to test if order_item raises exception if the product is out of stock"""
    with pytest.raises(InvalidOrderItemProductQtyException):
        product: ProductEntity = ProductEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0
        )
        OrderItemEntity.create(
            "f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1)
        )


def test_should_create():
    """Function to test if AN EXISTING order_item is created with right parameters"""
    product: ProductEntity = ProductEntity.create(
        "b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0
    )
    sut = OrderItemEntity.create(
        "f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1)
    )
    assert sut.id.value == "f3331752-6c11-4578-adb7-331d703cb445"
    assert sut.price == product.unit_price
    assert sut.qty == product.qty
    assert sut.product.id.value == product.id.value
    assert sut.created_at.timestamp() == 0


def test_should_create_new():
    """Function to test if A NON-EXISTING order_item is created with right parameters"""
    product: ProductEntity = ProductEntity.create(
        "b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0
    )
    sut = OrderItemEntity.create_new("f3331752-6c11-4578-adb7-331d703cb445", product)
    assert sut.id.value == "f3331752-6c11-4578-adb7-331d703cb445"
    assert sut.price == product.unit_price
    assert sut.qty == product.qty
    assert sut.product.id.value == product.id.value
    assert sut.created_at.timestamp() < datetime.now().timestamp()
