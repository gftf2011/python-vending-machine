import pytest
from datetime import datetime

from src.domain.entities.product import ProductEntity
from src.domain.entities.order_item import OrderItemEntity
from src.domain.entities.order import OrderEntity, OrderStatus

from src.domain.entities.payment import PaymentType

from src.domain.contracts.services.payment import PayForProductInputDTO

from src.services.payment import PaymentService

from src.services.exceptions.order_does_not_exist import OrderDoesNotExistException
from src.services.exceptions.not_enough_for_payment import NotEnoughForPaymentException

from src.infra.repositories.order.stub_order_repository import StubOrderRepository, FindByIdResponseWithSuccessObject
from src.infra.repositories.payment.dummy_payment_repository import DummyPaymentRepository

@pytest.mark.asyncio
async def test_should_raise_exception_if_order_is_not_found():
    with pytest.raises(OrderDoesNotExistException):
        order_repo = StubOrderRepository([FindByIdResponseWithSuccessObject(None)], [], [])
        payment_repo = DummyPaymentRepository()
        service = PaymentService(order_repo, payment_repo)
        input = PayForProductInputDTO("43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e", 0, PaymentType.CASH)
        await service.pay_for_product(input)

@pytest.mark.asyncio
async def test_should_raise_exception_if_product_amount_paid_is_insufficient():
    machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    product: ProductEntity = ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 1)
    order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1))]
    order = OrderEntity.create("f3331752-6c11-4578-adb7-331d703cb446", machine_id, order_items, OrderStatus.PENDING, datetime(1970, 1, 1), datetime(1970, 1, 1))
    with pytest.raises(NotEnoughForPaymentException):
        order_repo = StubOrderRepository([FindByIdResponseWithSuccessObject(order)], [], [])
        payment_repo = DummyPaymentRepository()
        service = PaymentService(order_repo, payment_repo)
        input = PayForProductInputDTO(order.get_id().get_value(), 0, PaymentType.CASH)
        await service.pay_for_product(input)