from abc import ABC, abstractmethod

from src.domain.entities.payment import PaymentEntity

class IPaymentRepository(ABC):
    @abstractmethod
    async def save(self, entity: PaymentEntity) -> None:
        raise NotImplementedError
