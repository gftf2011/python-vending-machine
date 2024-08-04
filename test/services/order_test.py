from datetime import datetime

import pytest

from src.domain.contracts.dtos.order import (
    CreateOrderInputDTO,
    DeliverOrderInputDTO,
)

from src.services.order import OrderService

from src.services.exceptions.unregistered_machine import UnregisteredMachineException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException
from src.services.exceptions.order_does_not_exist import OrderDoesNotExistException

from src.infra.repositories.machine.stub_machine_repository import (
    StubMachineRepository,
    FindByIdResponseWithSuccessObject as FindByIdMachineResponseWithSuccessObject,
)
from src.infra.repositories.machine.dummy_machine_repository import (
    DummyMachineRepository,
)
from src.infra.repositories.order.dummy_order_repository import DummyOrderRepository
from src.infra.repositories.order.stub_order_repository import (
    UpdateResponseWithSuccessObject as UpdateOrderResponseWithSuccessObject,
    FindByIdResponseWithSuccessObject as FindByIdOrderResponseWithSuccessObject,
    StubOrderRepository,
)

from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity
from src.domain.entities.order_item import OrderItemEntity
from src.domain.entities.order import OrderEntity, OrderStatus

from src.domain.exceptions.invalid_order_status_change import (
    InvalidOrderStatusChangeException,
)


class Test_Order_Service_Create:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_registered(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_qty: int = 0
        with pytest.raises(UnregisteredMachineException):
            machine_repo = StubMachineRepository(
                [FindByIdMachineResponseWithSuccessObject(None)], [], []
            )
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
            products = [
                ProductEntity.create(
                    "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4d", "Hersheys", 0, "01", 0
                )
            ]
            owner = OwnerEntity.create(
                "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4c",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdMachineResponseWithSuccessObject(machine)], [], []
            )
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
            owner = OwnerEntity.create(
                "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4c",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdMachineResponseWithSuccessObject(machine)], [], []
            )
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
        owner = OwnerEntity.create(
            "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4c", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
        )

        machine_repo = StubMachineRepository(
            [FindByIdMachineResponseWithSuccessObject(machine)], [], []
        )
        order_repo = DummyOrderRepository()

        service = OrderService(machine_repo, order_repo)
        input = CreateOrderInputDTO(machine_id, product_id, product_qty)

        output = await service.create(input)

        assert output.order_id is not None


class Test_Order_Service_Deliver_Order:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_order_does_not_exists(self):
        order_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(OrderDoesNotExistException):
            machine_repo = DummyMachineRepository()
            order_repo = StubOrderRepository(
                [FindByIdOrderResponseWithSuccessObject(None)], [], []
            )
            service = OrderService(machine_repo, order_repo)
            input = DeliverOrderInputDTO(order_id)
            await service.deliver_order(input)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_order_is_cancelled(self):
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
        product: ProductEntity = ProductEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0
        )
        order_items = [
            OrderItemEntity.create(
                "f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1)
            )
        ]
        order = OrderEntity.create(
            "f3331752-6c11-4578-adb7-331d703cb446",
            machine_id,
            order_items,
            OrderStatus.CANCELED,
            datetime(1970, 1, 1),
            datetime(1970, 1, 1),
        )
        with pytest.raises(InvalidOrderStatusChangeException):
            machine_repo = DummyMachineRepository()
            order_repo = StubOrderRepository(
                [FindByIdOrderResponseWithSuccessObject(order)],
                [],
                [],
            )
            service = OrderService(machine_repo, order_repo)
            input = DeliverOrderInputDTO(order.id.value)
            await service.deliver_order(input)

    @pytest.mark.asyncio
    async def test_should_update_order_status(self):
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
        product: ProductEntity = ProductEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "00", 0
        )
        order_items = [
            OrderItemEntity.create(
                "f3331752-6c11-4578-adb7-331d703cb445", product, datetime(1970, 1, 1)
            )
        ]
        order = OrderEntity.create(
            "f3331752-6c11-4578-adb7-331d703cb446",
            machine_id,
            order_items,
            OrderStatus.PENDING,
            datetime(1970, 1, 1),
            datetime(1970, 1, 1),
        )
        machine_repo = DummyMachineRepository()
        order_repo = StubOrderRepository(
            [FindByIdOrderResponseWithSuccessObject(order)],
            [],
            [UpdateOrderResponseWithSuccessObject()],
        )
        service = OrderService(machine_repo, order_repo)
        input = DeliverOrderInputDTO(order.id.value)
        await service.deliver_order(input)

        assert order.order_status == OrderStatus.DELIVERED
        assert order.created_at.timestamp() < order.updated_at.timestamp()
