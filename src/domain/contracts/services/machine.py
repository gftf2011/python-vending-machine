from abc import ABC, abstractmethod

from src.domain.contracts.dtos.machine import (
    ChooseProductInputDTO,
    ChooseProductOutputDTO,
    AddCoinsInputDTO,
    AddCoinsOutputDTO,
    AllowDispenseInputDTO,
    FinishDispenseInputDTO,
    DeliverProductInputDTO,
    DeliverProductOutputDTO,
)


class IMachineService(ABC):
    @abstractmethod
    async def choose_product(
        self, input_dto: ChooseProductInputDTO
    ) -> ChooseProductOutputDTO:
        """Function used to choose which product to be purchased"""
        raise NotImplementedError

    @abstractmethod
    async def add_coins(self, input_dto: AddCoinsInputDTO) -> AddCoinsOutputDTO:
        """Function used to update the number of coins the machine after the product payment"""
        raise NotImplementedError

    @abstractmethod
    async def allow_dispense(self, input_dto: AllowDispenseInputDTO) -> None:
        """Function used to update machine state to dispense a product"""
        raise NotImplementedError

    @abstractmethod
    async def finish_dispense(self, input_dto: FinishDispenseInputDTO) -> None:
        """Function used to update machine state to make it ready for a new operation"""
        raise NotImplementedError

    @abstractmethod
    async def deliver_product(
        self, input_dto: DeliverProductInputDTO
    ) -> DeliverProductOutputDTO:
        """Function used to deliver machine product quantity after payment"""
        raise NotImplementedError
