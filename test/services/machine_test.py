import pytest

from src.domain.entities.product import ProductEntity
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.contracts.services.machine import ChooseProductInputDTO

from src.services.machine import MachineService
from src.services.exceptions.unregistered_machine import UnregistredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException

from src.infra.repositories.machine.stub_machine_repository import FindByIdResponseWithSuccessObject, StubMachineRepository

@pytest.mark.asyncio
async def test_should_raise_exception_if_machine_is_not_registered():
    id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    with pytest.raises(UnregistredMachineException):
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(None)], [])
        service = MachineService(machine_repo)
        input = ChooseProductInputDTO("00", id)
        await service.choose_product(input)

@pytest.mark.asyncio
async def test_should_raise_exception_if_machine_is_not_ready():
    id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    with pytest.raises(MachineIsNotReadyException):
        products = []
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(id, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products)
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
        service = MachineService(machine_repo)
        input = ChooseProductInputDTO("00", id)
        await service.choose_product(input)

@pytest.mark.asyncio
async def test_should_raise_exception_if_product_is_not_found():
    product_code: str = "00"
    machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    with pytest.raises(ProductDoesNotExistException):
        products = []
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
        service = MachineService(machine_repo)
        input = ChooseProductInputDTO(product_code, machine_id)
        await service.choose_product(input)

@pytest.mark.asyncio
async def test_should_raise_exception_if_product_is_out_of_stock():
    product_code: str = "00"
    machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
    with pytest.raises(UnavailableProductException):
        products = [ProductEntity.create("a9651193-6c44-4568-bdb6-883d703cbee5", "Hersheys", 0, "00", 0)]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
        service = MachineService(machine_repo)
        input = ChooseProductInputDTO(product_code, machine_id)
        await service.choose_product(input)

@pytest.mark.asyncio
async def test_should_get_output():
    product_code: str = "00"
    machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"

    products = [ProductEntity.create("a9651193-6c44-4568-bdb6-883d703cbee5", "Hersheys", 1, "00", 0)]
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create(machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
    
    machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
    
    service = MachineService(machine_repo)
    input = ChooseProductInputDTO(product_code, machine_id)
    
    output = await service.choose_product(input)
    
    assert output.product_id == "a9651193-6c44-4568-bdb6-883d703cbee5"
    assert output.product_name == "Hersheys"
    assert output.product_price == 0
