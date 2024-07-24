from typing import Optional
from abc import ABC, abstractmethod

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.product import ProductEntity

class IProductRepository(ABC):
    @abstractmethod
    async def find_by_code(self, code: str, machine_id: UUIDValueObject) -> Optional[ProductEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: ProductEntity) -> None:
        raise NotImplementedError
