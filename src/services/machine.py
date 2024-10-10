from typing import Optional

from src.domain.entities.machine import MachineEntity, MachineState, CoinsChange
from src.domain.entities.product import ProductEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.machine import IMachineRepository

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

from src.domain.contracts.services.machine import (
    IMachineService,
)

from src.services.exceptions.unregistered_machine import UnregisteredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException
from src.services.exceptions.incorrect_negative_change import (
    IncorrectNegativeChangeException,
)
from src.services.exceptions.machine_is_not_dispensing import (
    MachineIsNotDispensingException,
)


class MachineService(IMachineService):
    def __init__(self, machine_repo: IMachineRepository):
        self.__machine_repo: IMachineRepository = machine_repo

    def __find_product_by_code(self, product_code: str, products: list[ProductEntity]) -> Optional[ProductEntity]:
        for product in products:
            if product_code == product.code:
                return product
        return None

    def __find_product_by_id(self, product_id: str, products: list[ProductEntity]) -> Optional[ProductEntity]:
        for product in products:
            if product_id == product.id.value:
                return product
        return None

    async def choose_product(self, input_dto: ChooseProductInputDTO) -> ChooseProductOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)
        if machine_found.state != MachineState.READY:
            raise MachineIsNotReadyException()

        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product_by_code(input_dto.product_code, products)

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty == 0:
            raise UnavailableProductException(product_found.id.value)

        return ChooseProductOutputDTO(product_found.id.value, product_found.unit_price, product_found.name)

    async def add_coins(self, input_dto: AddCoinsInputDTO) -> AddCoinsOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)
        if machine_found.state != MachineState.READY:
            raise MachineIsNotReadyException()

        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product_by_id(input_dto.product_id, products)

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty == 0:
            raise UnavailableProductException(product_found.id.value)

        amount: int = machine_found.get_amount_out_of_coins(
            input_dto.coin_01_qty,
            input_dto.coin_05_qty,
            input_dto.coin_10_qty,
            input_dto.coin_25_qty,
            input_dto.coin_50_qty,
            input_dto.coin_100_qty,
        )

        change: int = amount - product_found.unit_price

        if change < 0:
            raise IncorrectNegativeChangeException()

        machine_found.add_coins(
            input_dto.coin_01_qty,
            input_dto.coin_05_qty,
            input_dto.coin_10_qty,
            input_dto.coin_25_qty,
            input_dto.coin_50_qty,
            input_dto.coin_100_qty,
        )

        coins: CoinsChange = machine_found.get_coins_from_change(change)

        await self.__machine_repo.update(machine_found)

        return AddCoinsOutputDTO(
            coins.coin_01_qty,
            coins.coin_05_qty,
            coins.coin_10_qty,
            coins.coin_25_qty,
            coins.coin_50_qty,
            coins.coin_100_qty,
            product_found.unit_price,
        )

    async def allow_dispense(self, input_dto: AllowDispenseInputDTO) -> None:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)

        machine_found.start_dispense_product()

        await self.__machine_repo.update(machine_found)

    async def deliver_product(self, input_dto: DeliverProductInputDTO) -> DeliverProductOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)
        if machine_found.state != MachineState.DISPENSING:
            raise MachineIsNotDispensingException()

        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product_by_id(input_dto.product_id, products)

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty < input_dto.product_qty:
            raise UnavailableProductException(product_found.id.value)

        machine_found.deliver_product(product_found.id)

        await self.__machine_repo.update(machine_found)

        return DeliverProductOutputDTO(product_found.id.value, product_found.code)

    async def finish_dispense(self, input_dto: FinishDispenseInputDTO) -> None:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(
            UUIDValueObject.create(input_dto.machine_id)
        )
        if not machine_found:
            raise UnregisteredMachineException(input_dto.machine_id)

        machine_found.finish_dispense_product()

        await self.__machine_repo.update(machine_found)
