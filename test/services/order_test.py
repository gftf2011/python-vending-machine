import pytest

from src.domain.contracts.services.order import CreateOrderInputDTO

from src.services.order import OrderService

from src.services.exceptions.unregistered_machine import UnregistredMachineException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException

from src.infra.repositories.machine.stub_machine_repository import StubMachineRepository, FindByIdResponseWithSuccessObject
from src.infra.repositories.order.dummy_order_repository import DummyOrderRepository

from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity

class Test_Order_Service_Create:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_registered(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_qty: int = 0
        with pytest.raises(UnregistredMachineException):
            machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(None)], [])
            order_repo = DummyOrderRepository()
            service = OrderService(machine_repo, order_repo)
            input = CreateOrderInputDTO(machine_id, product_id, product_qty)
            await service.create(input)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_is_not_found(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_qty: int = 0
        with pytest.raises(ProductDoesNotExistException):
            products = [ProductEntity.create("43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4d", "Hersheys", 0, "01", 0)]
            owner = OwnerEntity.create("43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4c", "Sebastião Maia", "test@mail.com")
            machine = MachineEntity.create(machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
            machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
            order_repo = DummyOrderRepository()
            service = OrderService(machine_repo, order_repo)
            input = CreateOrderInputDTO(machine_id, product_id, product_qty)
            await service.create(input)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_quantity_is_not_enough(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_qty: int = 1
        with pytest.raises(UnavailableProductException):
            products = [ProductEntity.create(product_id, "Hersheys", 0, "01", 0)]
            owner = OwnerEntity.create("43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4c", "Sebastião Maia", "test@mail.com")
            machine = MachineEntity.create(machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
            machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
            order_repo = DummyOrderRepository()
            service = OrderService(machine_repo, order_repo)
            input = CreateOrderInputDTO(machine_id, product_id, product_qty)
            await service.create(input)


    @pytest.mark.asyncio
    async def test_should_return_order_id(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_qty: int = 1

        products = [ProductEntity.create(product_id, "Hersheys", 1, "01", 0)]
        owner = OwnerEntity.create("43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4c", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)

        machine_repo = StubMachineRepository([FindByIdResponseWithSuccessObject(machine)], [])
        order_repo = DummyOrderRepository()

        service = OrderService(machine_repo, order_repo)
        input = CreateOrderInputDTO(machine_id, product_id, product_qty)

        output = await service.create(input)
        
        assert output.order_id != None