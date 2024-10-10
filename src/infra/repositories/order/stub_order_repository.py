from abc import ABC, abstractmethod

from src.domain.repositories.order import IOrderRepository


class IFindByIdAndMachineIdResponseObject(ABC):
    @abstractmethod
    def execute(self, id, machine_id, created_at):
        pass


class FindByIdAndMachineIdResponseWithSuccessObject(IFindByIdAndMachineIdResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self, id, machine_id, created_at):
        return self.__response


class FindByIdAndMachineIdResponseWithFailureObject(IFindByIdAndMachineIdResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, id, machine_id, created_at):
        raise self.__response


class IUpdateResponseObject(ABC):
    @abstractmethod
    def execute(self, entity):
        pass


class UpdateResponseWithSuccessObject(IUpdateResponseObject):
    def execute(self, entity):
        return None


class UpdateResponseWithFailureObject(IUpdateResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, entity):
        raise self.__response


class ISaveResponseObject(ABC):
    @abstractmethod
    def execute(self, entity):
        pass


class SaveResponseWithSuccessObject(ISaveResponseObject):
    def execute(self, entity):
        return None


class SaveResponseWithFailureObject(ISaveResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, entity):
        raise self.__response


class StubOrderRepository(IOrderRepository):
    def __init__(
        self,
        find_by_id_response_list: list[IFindByIdAndMachineIdResponseObject],
        save_response_list: list[ISaveResponseObject],
        update_response_list: list[IUpdateResponseObject],
    ):
        self.__find_by_id_response_list = find_by_id_response_list
        self.__save_response_list = save_response_list
        self.__update_response_list = update_response_list
        self.__find_by_id_counter = 0
        self.__save_counter = 0
        self.__update_counter = 0

    async def find_by_id_and_machine_id(self, id, machine_id, created_at):
        aux_counter = self.__find_by_id_counter
        self.__find_by_id_counter += 1
        response = self.__find_by_id_response_list[aux_counter].execute(id, machine_id, created_at)
        return response

    async def update(self, entity):
        aux_counter = self.__update_counter
        self.__update_counter += 1
        self.__update_response_list[aux_counter].execute(entity)

    async def save(self, entity):
        aux_counter = self.__save_counter
        self.__save_counter += 1
        self.__save_response_list[aux_counter].execute(entity)
