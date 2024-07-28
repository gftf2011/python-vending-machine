from typing import Optional

from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.product import ProductEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.machine import IMachineRepository

from src.domain.contracts.services.machine import ChooseProductInputDTO, ChooseProductOutputDTO, IMachineService

from src.services.exceptions.unregistered_machine import UnregistredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException

class MachineService(IMachineService):
    def __init__(self, machine_repo: IMachineRepository):
        self.__machine_repo: IMachineRepository = machine_repo

    def __find_product(self, product_code: str, products: list[ProductEntity]) -> Optional[ProductEntity]:
        for product in products:
            if product_code == product.code:
                return product
        return None

    async def choose_product(self, input: ChooseProductInputDTO) -> ChooseProductOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(UUIDValueObject.create(input.machine_id))
        if not machine_found:
            raise UnregistredMachineException(input.machine_id)
        if machine_found.state != MachineState.READY:
            raise MachineIsNotReadyException()
        
        products: list[ProductEntity] = machine_found.products
        product_found: ProductEntity = self.__find_product(input.product_code, products)

        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.qty == 0:
            raise UnavailableProductException(product_found.id.value)

        return ChooseProductOutputDTO(product_found.id.value, product_found.unit_price, product_found.name)
