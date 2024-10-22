from typing import Any
from abc import ABC, abstractmethod

from src.services.contracts.controllers.machine import (
    IMachineController,
    ChooseProductInputControllerDTO,
    PayForProductInputControllerDTO,
)


class IChooseProductResponseObject(ABC):
    @abstractmethod
    def execute(self, input_dto: ChooseProductInputControllerDTO):
        pass


class ChooseProductResponseWithSuccessObject(IChooseProductResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self, input_dto: ChooseProductInputControllerDTO):
        return self.__response


class ChooseProductResponseWithFailureObject(IChooseProductResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, input_dto: ChooseProductInputControllerDTO):
        raise self.__response


class IPayForProductResponseObject(ABC):
    @abstractmethod
    def execute(self, input_dto: PayForProductInputControllerDTO):
        pass


class PayForProductResponseWithSuccessObject(IPayForProductResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self, input_dto: PayForProductInputControllerDTO):
        return self.__response


class PayForProductResponseWithFailureObject(IPayForProductResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, input_dto: PayForProductInputControllerDTO):
        raise self.__response


class StubMachineController(IMachineController):
    def __init__(
        self,
        choose_product_response_list: list[IChooseProductResponseObject],
        pay_for_product_response_list: list[IPayForProductResponseObject],
    ):
        self.__choose_product_response_list = choose_product_response_list
        self.__pay_for_product_response_list = pay_for_product_response_list
        self.__choose_product_counter = 0
        self.__pay_for_product_counter = 0

    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        aux_counter = self.__choose_product_counter
        self.__choose_product_counter += 1
        response = self.__choose_product_response_list[aux_counter].execute(input_dto)
        return response

    async def pay_for_product(self, input_dto: PayForProductInputControllerDTO) -> Any:
        aux_counter = self.__pay_for_product_counter
        self.__pay_for_product_counter += 1
        response = self.__pay_for_product_response_list[aux_counter].execute(input_dto)
        return response
