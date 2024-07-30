from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.machine import MachineEntity, MachineState, CoinsChange
from src.domain.entities.product import ProductEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.machine import IMachineRepository

from src.domain.contracts.services.machine import (
    ChooseProductInputDTO,
    ChooseProductOutputDTO,
    IMachineService,
    AddCoinsInputDTO,
    AddCoinsOutputDTO,
    AllowDispenseInputDTO,
)

from src.services.exceptions.unregistered_machine import UnregisteredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException
from src.services.exceptions.incorrect_negative_change import (
    IncorrectNegativeChangeException,
)


class _AddCoinsBasedOnChangeStrategy(ABC):
    @abstractmethod
    async def execute(
        self, machine: MachineEntity, input_dto: AddCoinsInputDTO
    ) -> AddCoinsOutputDTO:
        """Function used to execute the strategy to update a machine coins quantity based on the change given"""
        pass


class _AddCoinsWhenHasChangeToReturnStrategy(_AddCoinsBasedOnChangeStrategy):
    def __init__(self, machine_repo: IMachineRepository) -> None:
        self.__machine_repo = machine_repo

    async def execute(
        self, machine: MachineEntity, input_dto: AddCoinsInputDTO
    ) -> AddCoinsOutputDTO:
        machine.add_coins(
            input_dto.coin_01_qty,
            input_dto.coin_05_qty,
            input_dto.coin_10_qty,
            input_dto.coin_25_qty,
            input_dto.coin_50_qty,
            input_dto.coin_100_qty,
        )
        coins: CoinsChange = machine.get_coins_from_change(input_dto.change)

        await self.__machine_repo.update(machine)

        return AddCoinsOutputDTO(
            coins.coin_01_qty,
            coins.coin_05_qty,
            coins.coin_10_qty,
            coins.coin_25_qty,
            coins.coin_50_qty,
            coins.coin_100_qty,
        )


class _AddCoinsWhenHasNOChangeToReturnStrategy(_AddCoinsBasedOnChangeStrategy):
    def __init__(self, machine_repo: IMachineRepository) -> None:
        self.__machine_repo = machine_repo

    async def execute(
        self, machine: MachineEntity, input_dto: AddCoinsInputDTO
    ) -> AddCoinsOutputDTO:
        machine.add_coins(
            input_dto.coin_01_qty,
            input_dto.coin_05_qty,
            input_dto.coin_10_qty,
            input_dto.coin_25_qty,
            input_dto.coin_50_qty,
            input_dto.coin_100_qty,
        )

        await self.__machine_repo.update(machine)

        return AddCoinsOutputDTO(0, 0, 0, 0, 0, 0)


class _DontAddCoinsWhenChangeIsNegativeToReturnStrategy(_AddCoinsBasedOnChangeStrategy):
    def __init__(self, machine_repo: IMachineRepository) -> None:
        self.__machine_repo = machine_repo

    async def execute(
        self, machine: MachineEntity, input_dto: AddCoinsInputDTO
    ) -> AddCoinsOutputDTO:
        raise IncorrectNegativeChangeException()


class _AddCoinsStrategyContext(_AddCoinsBasedOnChangeStrategy):
    def __init__(self, machine_repo: IMachineRepository) -> None:
        self.__machine_repo = machine_repo

    async def execute(
        self, machine: MachineEntity, input_dto: AddCoinsInputDTO
    ) -> AddCoinsOutputDTO:
        if input_dto.change < 0:
            return await _DontAddCoinsWhenChangeIsNegativeToReturnStrategy(
                self.__machine_repo
            ).execute(machine, input_dto)
        elif input_dto.change == 0:
            return await _AddCoinsWhenHasNOChangeToReturnStrategy(
                self.__machine_repo
            ).execute(machine, input_dto)
        else:
            return await _AddCoinsWhenHasChangeToReturnStrategy(
                self.__machine_repo
            ).execute(machine, input_dto)


class MachineService(IMachineService):
    def __init__(self, machine_repo: IMachineRepository):
        self.__machine_repo: IMachineRepository = machine_repo

    def __find_product(
        self, product_code: str, products: list[ProductEntity]
    ) -> Optional[ProductEntity]:
        for product in products:
            if product_code == product.code:
                return product
        return None

    async def choose_product(
        self, input_dto: ChooseProductInputDTO
    ) -> ChooseProductOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)
        if machine_found.state != MachineState.READY:
            raise MachineIsNotReadyException()

        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product(
            input_dto.product_code, products
        )

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty == 0:
            raise UnavailableProductException(product_found.id.value)

        return ChooseProductOutputDTO(
            product_found.id.value, product_found.unit_price, product_found.name
        )

    async def add_coins(self, input_dto: AddCoinsInputDTO) -> AddCoinsOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)
        if machine_found.state != MachineState.READY:
            raise MachineIsNotReadyException()

        return await _AddCoinsStrategyContext(self.__machine_repo).execute(
            machine_found, input_dto
        )

    async def allow_dispense(self, input_dto: AllowDispenseInputDTO) -> None:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)

        machine_found.start_dispense_product()

        await self.__machine_repo.update(machine_found)
