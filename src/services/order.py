from typing import Optional
from datetime import datetime

from src.domain.entities.machine import MachineEntity
from src.domain.entities.product import ProductEntity
from src.domain.entities.order_item import OrderItemEntity
from src.domain.entities.order import OrderEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.machine import IMachineRepository
from src.domain.repositories.order import IOrderRepository

from src.domain.contracts.dtos.order import (
    CreateOrderInputDTO,
    CreateOrderOutputDTO,
    DeliverOrderInputDTO,
)

from src.domain.contracts.services.order import (
    IOrderService,
)

from src.services.exceptions.unregistered_machine import UnregisteredMachineException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException
from src.services.exceptions.order_does_not_exist import OrderDoesNotExistException


class OrderService(IOrderService):
    def __init__(self, machine_repo: IMachineRepository, order_repo: IOrderRepository):
        self.__machine_repo: IMachineRepository = machine_repo
        self.__order_repo: IOrderRepository = order_repo

    def __find_product(self, product_id: str, products: list[ProductEntity]) -> Optional[ProductEntity]:
        for product in products:
            if product_id == product.id.value:
                return product
        return None

    async def create(self, input_dto: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)

        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product(input_dto.product_id, products)

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty < input_dto.product_qty:
            raise UnavailableProductException(product_found.id.value)

        product_order: ProductEntity = ProductEntity.create(
            product_found.id.value,
            product_found.name,
            input_dto.product_qty,
            product_found.code,
            product_found.unit_price,
        )
        order_item: OrderItemEntity = OrderItemEntity.create_new(
            UUIDValueObject.create_new().value, input_dto.product_qty, product_order
        )
        order: OrderEntity = OrderEntity.create_new(
            UUIDValueObject.create_new().value, input_dto.machine_id, [order_item]
        )

        await self.__order_repo.save(order)

        return CreateOrderOutputDTO(order.id.value)

    async def deliver_order(self, input_dto: DeliverOrderInputDTO) -> None:
        order_found: OrderEntity = await self.__order_repo.find_by_id_and_machine_id(
            UUIDValueObject.create(input_dto.order_id),
            UUIDValueObject.create(input_dto.machine_id),
            datetime.fromisoformat(input_dto.order_created_at),
        )
        if not order_found:
            raise OrderDoesNotExistException(input_dto.order_id)

        order_found.deliver_order()

        await self.__order_repo.update(order_found)
