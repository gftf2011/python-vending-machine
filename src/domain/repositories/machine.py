from typing import Optional
from abc import ABC, abstractmethod

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.machine import MachineEntity

class IMachineRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: UUIDValueObject) -> Optional[MachineEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: MachineEntity) -> None:
        raise NotImplementedError
