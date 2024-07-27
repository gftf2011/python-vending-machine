import pytest

from src.domain.entities.payment import PaymentType

from src.domain.contracts.services.payment import PayForProductInputDTO

from src.services.payment import PaymentService

from src.services.exceptions.order_does_not_exist import OrderDoesNotExistException

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