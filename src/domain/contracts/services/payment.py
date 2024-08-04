from abc import ABC, abstractmethod

from src.domain.contracts.dtos.payment import (
    PayForProductInputDTO,
    PayForProductOutputDTO,
)


class IPaymentService(ABC):
    @abstractmethod
    async def pay_for_product(
        self, input_dto: PayForProductInputDTO
    ) -> PayForProductOutputDTO:
        """Function used to create the payment for chosen product"""
        raise NotImplementedError
