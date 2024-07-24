import pytest

from src.domain.entities.owner import OwnerEntity
from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.contracts.services.machine import ChooseProductInputDTO

from src.services.machine import MachineService
from src.services.exceptions.unregistered_machine import UnregistredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException

from src.infra.repositories.machine.stub_machine_repository import FindByIdResponseWithSuccessObject, StubMachineRepository
from src.infra.repositories.product.dummy_product_repository import DummyProductRepository

@pytest.mark.asyncio
async def test_should_raise_exception_if_machine_is_not_registered():
    id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    with pytest.raises(UnregistredMachineException, match='machine - "' + id + '" - is not registered in the system'):
        product_repo = DummyProductRepository()
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(None)], [])
        service = MachineService(machine_repo, product_repo)
        input = ChooseProductInputDTO("00", id)
        await service.choose_product(input)

@pytest.mark.asyncio
async def test_should_raise_exception_if_machine_is_not_ready():
    id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    with pytest.raises(MachineIsNotReadyException, match="machine is not READY for operation"):
        products = []
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(id, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products)
        product_repo = DummyProductRepository()
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
        service = MachineService(machine_repo, product_repo)
        input = ChooseProductInputDTO("00", id)
        await service.choose_product(input)
