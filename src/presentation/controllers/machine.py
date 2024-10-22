from typing import Any

from src.domain.contracts.dtos.base import BaseOutput

from src.domain.contracts.dtos.machine import (
    ChooseProductOutputDTO,
    ChooseProductInputDTO,
    AddCoinsInputDTO,
    AllowDispenseInputDTO,
    DeliverProductInputDTO,
    FinishDispenseInputDTO,
)
from src.domain.contracts.dtos.order import CreateOrderInputDTO, CreateOrderOutputDTO
from src.domain.contracts.dtos.payment import (
    PayForProductInputDTO,
)

from src.domain.contracts.services.machine import IMachineService
from src.domain.contracts.services.order import IOrderService
from src.domain.contracts.services.payment import IPaymentService

from src.services.contracts.controllers.machine import (
    ChooseProductInputControllerDTO,
    PayForProductInputControllerDTO,
    IMachineController,
)

from src.presentation.contracts.presenters.base import BasePresenter


class ChooseProductErrorOutputControllerDTO(BaseOutput):
    def __init__(self, message: str):
        self.message = message

    def to_dict(self) -> Any:
        return {"error": {"message": self.message}}


class PayForProductErrorOutputControllerDTO(BaseOutput):
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


class MachineController(IMachineController):
    def __init__(
        self,
        presenter: BasePresenter,
        machine_service: IMachineService,
        order_service: IOrderService,
        payment_service: IPaymentService,
    ):
        self._presenter = presenter
        self._machine_service = machine_service
        self._order_service = order_service
        self._payment_service = payment_service

    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        try:
            output: ChooseProductOutputDTO = await self._machine_service.choose_product(
                ChooseProductInputDTO(input_dto.product_code, input_dto.machine_id)
            )
            return self._presenter.execute(output), 200
        except Exception as error:
            if (
                type(error).__name__ == "UnregisteredMachineException"
                or type(error).__name__ == "ProductDoesNotExistException"
                or type(error).__name__ == "UnavailableProductException"
            ):
                return self._presenter.execute(ChooseProductErrorOutputControllerDTO(str(error))), 404
            if type(error).__name__ == "MachineIsNotReadyException":
                return self._presenter.execute(ChooseProductErrorOutputControllerDTO(str(error))), 400
            return self._presenter.execute(ChooseProductErrorOutputControllerDTO(str(error))), 500

    async def pay_for_product(self, input_dto: PayForProductInputControllerDTO) -> Any:
        try:
            add_coins_output = await self._machine_service.add_coins(
                AddCoinsInputDTO(
                    input_dto.machine_id,
                    input_dto.product_id,
                    input_dto.coin_01_qty,
                    input_dto.coin_05_qty,
                    input_dto.coin_10_qty,
                    input_dto.coin_25_qty,
                    input_dto.coin_50_qty,
                    input_dto.coin_100_qty,
                )
            )
            create_order_output: CreateOrderOutputDTO = await self._order_service.create(
                CreateOrderInputDTO(input_dto.machine_id, input_dto.product_id, input_dto.product_qty)
            )
            await self._payment_service.pay_for_product(
                PayForProductInputDTO(
                    create_order_output.order_id,
                    input_dto.machine_id,
                    add_coins_output.amount_paid,
                    input_dto.payment_type,
                    input_dto.order_created_at,
                )
            )
            await self._machine_service.allow_dispense(AllowDispenseInputDTO(input_dto.machine_id))
            await self._machine_service.deliver_product(
                DeliverProductInputDTO(input_dto.machine_id, input_dto.product_id, input_dto.product_qty)
            )
            await self._machine_service.finish_dispense(FinishDispenseInputDTO(input_dto.machine_id))
            return self._presenter.execute(add_coins_output), 201
        except Exception as error:
            if type(error).__name__ == "MachineIsNotReadyException":
                return (
                    self._presenter.execute(
                        PayForProductErrorOutputControllerDTO(
                            str(error),
                            input_dto.coin_01_qty,
                            input_dto.coin_05_qty,
                            input_dto.coin_10_qty,
                            input_dto.coin_25_qty,
                            input_dto.coin_50_qty,
                            input_dto.coin_100_qty,
                        )
                    ),
                    400,
                )
            if (
                type(error).__name__ == "UnregisteredMachineException"
                or type(error).__name__ == "ProductDoesNotExistException"
                or type(error).__name__ == "UnavailableProductException"
                or type(error).__name__ == "NoChangeAvailableException"
            ):
                return (
                    self._presenter.execute(
                        PayForProductErrorOutputControllerDTO(
                            str(error),
                            input_dto.coin_01_qty,
                            input_dto.coin_05_qty,
                            input_dto.coin_10_qty,
                            input_dto.coin_25_qty,
                            input_dto.coin_50_qty,
                            input_dto.coin_100_qty,
                        )
                    ),
                    404,
                )
            if type(error).__name__ == "IncorrectNegativeChangeException":
                return (
                    self._presenter.execute(
                        PayForProductErrorOutputControllerDTO(
                            str(error),
                            input_dto.coin_01_qty,
                            input_dto.coin_05_qty,
                            input_dto.coin_10_qty,
                            input_dto.coin_25_qty,
                            input_dto.coin_50_qty,
                            input_dto.coin_100_qty,
                        )
                    ),
                    416,
                )
            return (
                self._presenter.execute(
                    PayForProductErrorOutputControllerDTO(
                        str(error),
                        input_dto.coin_01_qty,
                        input_dto.coin_05_qty,
                        input_dto.coin_10_qty,
                        input_dto.coin_25_qty,
                        input_dto.coin_50_qty,
                        input_dto.coin_100_qty,
                    )
                ),
                500,
            )
