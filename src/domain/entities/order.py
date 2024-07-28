from enum import Enum
from datetime import datetime
from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.order_item import OrderItemEntity

from src.domain.exceptions.invalid_order_status_change import InvalidOrderStatusChangeException

class OrderStatus(Enum):
    PENDING = 'PENDING'
    DELIVERED = 'DELIVERED'
    CANCELED = 'CANCELED'

class OrderEntity:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' OR 'create_new' methods to create an instance of this class.")

    def __init__(self, id: str, machine_id: str, order_items: list[OrderItemEntity], total_amount: int, order_status: OrderStatus, created_at: datetime, updated_at: datetime):
        self.__id: UUIDValueObject = UUIDValueObject.create(id)
        self.__machine_id: UUIDValueObject = UUIDValueObject.create(machine_id)
        self.__order_items: list[OrderItemEntity] = order_items
        self.__total_amount: int = total_amount
        self.__order_status: OrderStatus = order_status
        self.__created_at: datetime = created_at
        self.__updated_at: datetime = updated_at

    @classmethod
    def create(cls, id: str, machine_id: str, order_items: list[OrderItemEntity], order_status: OrderStatus, created_at: datetime, updated_at: datetime) -> Self:
        instance = super().__new__(cls)
        total_amount: int = 0
        for order_item in order_items:
            total_amount += order_item.get_price()
        instance.__init__(id, machine_id, order_items, total_amount, order_status, created_at, updated_at)
        return instance

    @classmethod
    def create_new(cls, id: str, machine_id: str, order_items: list[OrderItemEntity]) -> Self:
        instance = super().__new__(cls)
        timestamp: datetime = datetime.now()
        created_at: datetime = timestamp
        updated_at: datetime = timestamp
        order_status: OrderStatus = OrderStatus.PENDING
        total_amount: int = 0
        for order_item in order_items:
            total_amount += order_item.get_price()
        instance.__init__(id, machine_id, order_items, total_amount, order_status, created_at, updated_at)
        return instance

    def get_id(self) -> UUIDValueObject:
        return self.__id

    def get_machine_id(self) -> UUIDValueObject:
        return self.__machine_id

    def get_order_items(self) -> list[OrderItemEntity]:
        return self.__order_items

    def get_order_status(self) -> OrderStatus:
        return self.__order_status

    def get_created_at(self) -> datetime:
        return self.__created_at

    def get_updated_at(self) -> datetime:
        return self.__updated_at

    def get_total_amount(self) -> int:
        return self.__total_amount

    def deliver_order(self) -> None:
        if self.__order_status == OrderStatus.CANCELED:
            raise InvalidOrderStatusChangeException(self.__id.value)
        self.__order_status = OrderStatus.DELIVERED
        self.__updated_at = datetime.now()

    def cancel_order(self) -> None:
        if self.__order_status == OrderStatus.DELIVERED:
            raise InvalidOrderStatusChangeException(self.__id.value)
        self.__order_status = OrderStatus.CANCELED
        self.__updated_at = datetime.now()