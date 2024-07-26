import pytest

from src.domain.contracts.services.order import CreateOrderInputDTO

from src.services.order import OrderService

from src.services.exceptions.unregistered_machine import UnregistredMachineException

from src.infra.repositories.machine.stub_machine_repository import StubMachineRepository, FindByIdResponseWithSuccessObject
from src.infra.repositories.order.dummy_order_repository import DummyOrderRepository

@pytest.mark.asyncio
async def test_should_raise_exception_if_machine_is_not_registered():
    machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
    product_qty: int = 0
    with pytest.raises(UnregistredMachineException):
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(None)], [])
        order_repo = DummyOrderRepository()
        service = OrderService(machine_repo, order_repo)
        input = CreateOrderInputDTO(machine_id, product_id, product_qty)
        await service.create(input)