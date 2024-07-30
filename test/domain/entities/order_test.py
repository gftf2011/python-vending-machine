import pytest
from datetime import datetime

from src.domain.entities.order import OrderEntity, OrderStatus
from src.domain.entities.order_item import OrderItemEntity
from src.domain.entities.product import ProductEntity

from src.domain.exceptions.invalid_order_status_change import InvalidOrderStatusChangeException

def test_should_raise_exception_by_using_constructor():
    """Function to test if the software component will raise an exception if calls the constructor"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    with pytest.raises(Exception, match="Use the 'create' OR 'create_new' methods to create an instance of this class."):
        product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
        order_item = OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))
        OrderEntity("f3331752-6c11-4578-adb7-331d703cb446", machine_id, [order_item], order_item.price, OrderStatus.PENDING, datetime(1970, 1, 1),datetime(1970, 1, 1))

def test_should_create():
    """Function to test if AN EXISTING order is created with right parameters"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    sut = OrderEntity.create("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items, OrderStatus.PENDING, datetime(1970, 1, 1), datetime(1970, 1, 1))

    total_amount: int = 0
    for order_item in order_items:
        total_amount += order_item.price

    assert sut.id.value == "f3331752-6c11-4578-adb7-331d703cb446"
    assert sut.created_at.timestamp() == datetime(1970, 1, 1).timestamp()
    assert sut.updated_at.timestamp() == datetime(1970, 1, 1).timestamp()
    assert sut.machine_id.value == machine_id
    assert sut.order_items[0].id.value == "f3331752-6c11-4578-adb7-331d703cb445"
    assert sut.order_status == OrderStatus.PENDING
    assert sut.total_amount == total_amount

def test_should_create_new():
    """Function to test if A NON-EXISTING order is created with right parameters"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    sut = OrderEntity.create_new("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items)

    total_amount: int = 0
    for order_item in order_items:
        total_amount += order_item.price

    timestamp = datetime.now().timestamp()

    assert sut.id.value == "f3331752-6c11-4578-adb7-331d703cb446"
    assert sut.created_at.timestamp() < timestamp
    assert sut.updated_at.timestamp() < timestamp
    assert sut.machine_id.value == machine_id
    assert sut.order_items[0].id.value == "f3331752-6c11-4578-adb7-331d703cb445"
    assert sut.order_status == OrderStatus.PENDING
    assert sut.total_amount == total_amount

def test_should_raise_exception_when_try_to_cancel_order_when_order_is_delivered():
    """Function to test if order will raise exception if when try to cancel an order that is already delivered"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    with pytest.raises(InvalidOrderStatusChangeException):
        sut = OrderEntity.create("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items, OrderStatus.DELIVERED, datetime(1970, 1, 1), datetime(1970, 1, 1))
        sut.cancel_order()

def test_should_raise_exception_when_try_to_deliver_order_when_order_is_canceled():
    """Function to test if order will raise exception if when try to deliver an order that is already canceled"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    with pytest.raises(InvalidOrderStatusChangeException):
        sut = OrderEntity.create("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items, OrderStatus.CANCELED, datetime(1970, 1, 1), datetime(1970, 1, 1))
        sut.deliver_order()

def test_should_deliver_order():
    """Function to test if deliver_order function will change order to DELIVERED"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    sut = OrderEntity.create("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items, OrderStatus.PENDING, datetime(1970, 1, 1), datetime(1970, 1, 1))
    sut.deliver_order()
    assert sut.order_status == OrderStatus.DELIVERED

def test_should_cancel_order():
    """Function to test if cancel_order function will change order to CANCELED"""
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    sut = OrderEntity.create("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items, OrderStatus.PENDING, datetime(1970, 1, 1), datetime(1970, 1, 1))
    sut.cancel_order()
    assert sut.order_status == OrderStatus.CANCELED
