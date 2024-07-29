from typing import Optional

from src.domain.entities.machine import MachineEntity
from src.domain.entities.product import ProductEntity
from src.domain.entities.order_item import OrderItemEntity
from src.domain.entities.order import OrderEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.machine import IMachineRepository
from src.domain.repositories.order import IOrderRepository

from src.domain.contracts.services.order import CreateOrderInputDTO, CreateOrderOutputDTO, IOrderService

from src.services.exceptions.unregistered_machine import UnregisteredMachineException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException

class OrderService(IOrderService):
    def __init__(self, machine_repo: IMachineRepository, order_repo: IOrderRepository):
        self.__machine_repo: IMachineRepository = machine_repo
        self.__order_repo: IOrderRepository = order_repo

    def __find_product(self, product_id: str, products: list[ProductEntity]) -> Optional[ProductEntity]:
        for product in products:
            if product_id == product.id.value:
                return product
        return None

    async def create(self, input: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(UUIDValueObject.create(input.machine_id))
        if not machine_found:
            raise UnregisteredMachineException(input.machine_id)

        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product(input.product_id, products)

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty < input.product_qty:
            raise UnavailableProductException(product_found.id.value)

        product_order: ProductEntity = ProductEntity.create(product_found.id.value, product_found.name, input.product_qty, product_found.code, product_found.unit_price)
        order_item: OrderItemEntity = OrderItemEntity.create_new(UUIDValueObject.create_new().value, product_order)
        order: OrderEntity = OrderEntity.create_new(UUIDValueObject.create_new().value, input.machine_id, [order_item])

        await self.__order_repo.save(order)

        return CreateOrderOutputDTO(order.id.value)
