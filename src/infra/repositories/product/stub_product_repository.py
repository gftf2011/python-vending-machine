from abc import ABC, abstractmethod

from src.domain.repositories.product import IProductRepository

class IFindByCodeResponseObject(ABC):
    @abstractmethod
    def execute(self, code, machine_id):
        pass

class FindByCodeResponseWithSuccessObject(IFindByCodeResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self, code, machine_id):
        return self.__response

class FindByCodeResponseWithFailureObject(IFindByCodeResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, code, machine_id):
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

class StubProductRepository(IProductRepository):
    def __init__(self, find_by_code_response_list: list[IFindByCodeResponseObject], update_response_list: list[IUpdateResponseObject]):
        self.__find_by_code_response_list = find_by_code_response_list
        self.__update_response_list = update_response_list
        self.__find_by_code_counter = 0
        self.__update_counter = 0

    async def find_by_code(self, code, machine_id):
        aux_counter = self.__find_by_code_counter
        self.__find_by_code_counter += 1
        response = self.__find_by_code_response_list[aux_counter].execute(code, machine_id)
        return response

    async def update(self, entity):
        aux_counter = self.__update_counter
        self.__update_counter += 1
        self.__update_response_list[aux_counter].execute(entity)
