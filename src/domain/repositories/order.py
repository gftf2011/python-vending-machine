from typing import Optional
from abc import ABC, abstractmethod

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.order import OrderEntity


class IOrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: UUIDValueObject) -> Optional[OrderEntity]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, entity: OrderEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: OrderEntity) -> None:
        raise NotImplementedError
