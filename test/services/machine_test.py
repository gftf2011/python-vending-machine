import pytest

from src.domain.contracts.services.machine import ChooseProductInputDTO

from src.services.machine import MachineService
from src.services.exceptions.unregistered_machine import UnregistredMachineException

from src.infra.repositories.machine.stub_machine_repository import FindByIdResponseWithSuccessObject, StubMachineRepository
from src.infra.repositories.product.dummy_product_repository import DummyProductRepository

@pytest.mark.asyncio
async def test_should_raise_exception_if_machine_is_not_registered():
    with pytest.raises(UnregistredMachineException):
        product_repo = DummyProductRepository()
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(None)], [])
        service = MachineService(machine_repo, product_repo)
        input = ChooseProductInputDTO("00", "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e")
        await service.choose_product(input)
