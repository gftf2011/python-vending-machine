from typing import Any

from src.domain.contracts.dtos.base import BaseOutput

from src.domain.contracts.dtos.machine import (
    ChooseProductOutputDTO,
    ChooseProductInputDTO,
    AddCoinsInputDTO,
)

from src.domain.contracts.services.machine import IMachineService

from src.presentation.contracts.presenters.base import BasePresenter


class ChooseProductInputControllerDTO:
    def __init__(self, product_code: str):
        self.product_code = product_code


class AddCoinsInputControllerDTO:
    def __init__(
        self,
        product_id: str,
        coin_01_qty: int,
        coin_05_qty: int,
        coin_10_qty: int,
        coin_25_qty: int,
        coin_50_qty: int,
        coin_100_qty: int,
    ):
        self.product_id = product_id
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty


class ChooseProductErrorOutputControllerDTO(BaseOutput):
    def __init__(self, message: str):
        self.message = message

    def to_dict(self) -> Any:
        return {"error": {"message": self.message}}


class AddCoinsErrorOutputControllerDTO(BaseOutput):
    def __init__(
        self,
        message: str,
        coin_01_qty: int,
        coin_05_qty: int,
        coin_10_qty: int,
        coin_25_qty: int,
        coin_50_qty: int,
        coin_100_qty: int,
    ):
        self.message = message
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty

    def to_dict(self) -> Any:
        return {
            "error": {
                "message": self.message,
                "data": {
                    "coin_01": self.coin_01_qty,
                    "coin_05": self.coin_05_qty,
                    "coin_10": self.coin_10_qty,
                    "coin_25": self.coin_25_qty,
                    "coin_50": self.coin_50_qty,
                    "coin_100": self.coin_100_qty,
                },
            }
        }


class MachineController:
    def __init__(
        self,
        presenter: BasePresenter,
        machine_service: IMachineService,
        machine_id: str,
    ):
        self._presenter = presenter
        self._machine_service = machine_service
        self._machine_id = machine_id

    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        try:
            output: ChooseProductOutputDTO = await self._machine_service.choose_product(
                ChooseProductInputDTO(input_dto.product_code, self._machine_id)
            )
            return self._presenter.execute(output)
        except Exception as error:
            return self._presenter.execute(
                ChooseProductErrorOutputControllerDTO(str(error))
            )

    async def add_coins(self, input_dto: AddCoinsInputControllerDTO) -> Any:
        try:
            output = await self._machine_service.add_coins(
                AddCoinsInputDTO(
                    self._machine_id,
                    input_dto.product_id,
                    input_dto.coin_01_qty,
                    input_dto.coin_05_qty,
                    input_dto.coin_10_qty,
                    input_dto.coin_25_qty,
                    input_dto.coin_50_qty,
                    input_dto.coin_100_qty,
                )
            )
            return self._presenter.execute(output)
        except Exception as error:
            return self._presenter.execute(
                AddCoinsErrorOutputControllerDTO(
                    str(error),
                    input_dto.coin_01_qty,
                    input_dto.coin_05_qty,
                    input_dto.coin_10_qty,
                    input_dto.coin_25_qty,
                    input_dto.coin_50_qty,
                    input_dto.coin_100_qty,
                )
            )
