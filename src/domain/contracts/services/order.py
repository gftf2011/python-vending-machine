from abc import ABC, abstractmethod

from src.domain.contracts.dtos.order import (
    CreateOrderInputDTO,
    CreateOrderOutputDTO,
    DeliverOrderInputDTO,
)


class IOrderService(ABC):
    @abstractmethod
    async def create(self, input_dto: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        """Function used to create an order"""
        raise NotImplementedError

    @abstractmethod
    async def deliver_order(self, input_dto: DeliverOrderInputDTO) -> None:
        """Function used to update order to DELIVERED status"""
        raise NotImplementedError
