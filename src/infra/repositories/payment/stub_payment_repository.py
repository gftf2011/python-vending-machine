from abc import ABC, abstractmethod

from src.domain.repositories.payment import IPaymentRepository

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

class StubPaymentRepository(IPaymentRepository):
    def __init__(self, save_response_list: list[ISaveResponseObject]):
        self.__save_response_list = save_response_list
        self.__save_counter = 0

    async def save(self, entity):
        aux_counter = self.__save_counter
        self.__save_counter += 1
        self.__save_response_list[aux_counter].execute(entity)
