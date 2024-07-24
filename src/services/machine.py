from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.product import ProductEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.machine import IMachineRepository
from src.domain.repositories.product import IProductRepository

from src.domain.contracts.services.machine import ChooseProductInputDTO, ChooseProductOutputDTO, IMachineService

from src.services.exceptions.unregistered_machine import UnregistredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException

class MachineService(IMachineService):
    def __init__(self, machine_repo: IMachineRepository, product_repo: IProductRepository):
        self.__machine_repo: IMachineRepository = machine_repo
        self.__product_repo: IProductRepository = product_repo

    async def choose_product(self, input: ChooseProductInputDTO) -> ChooseProductOutputDTO:
        machine_found: MachineEntity = await self.__machine_repo.find_by_id(UUIDValueObject.create(input.machine_id))
        if not machine_found:
            raise UnregistredMachineException(input.machine_id)
        if machine_found.get_state() != MachineState.READY:
            raise MachineIsNotReadyException()
        
        product_found: ProductEntity = await self.__product_repo.find_by_code(input.product_code, machine_found.get_id())
        if not product_found:
            raise ProductDoesNotExistException()
        if product_found.get_qty() == 0:
            raise UnavailableProductException(product_found.get_id().get_value())

        return ChooseProductOutputDTO(product_found.get_id().get_value(), product_found.get_unit_price(), product_found.get_name())