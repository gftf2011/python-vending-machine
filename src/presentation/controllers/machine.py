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
from src.domain.entities.payment import PaymentType

from src.domain.contracts.services.machine import IMachineService
from src.domain.contracts.services.order import IOrderService
from src.domain.contracts.services.payment import IPaymentService

from src.presentation.contracts.presenters.base import BasePresenter


class ChooseProductInputControllerDTO:
    def __init__(self, product_code: str):
        self.product_code = product_code


class PayForProductInputControllerDTO:
    def __init__(
        self,
        machine_id: str,
        product_id: str,
        product_qty: int,
        payment_type: PaymentType,
        coin_01_qty: int,
        coin_05_qty: int,
        coin_10_qty: int,
        coin_25_qty: int,
        coin_50_qty: int,
        coin_100_qty: int,
        order_created_at: str,
    ):
        self.machine_id = machine_id
        self.product_id = product_id
        self.product_qty = product_qty
        self.payment_type = payment_type
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty
        self.order_created_at = order_created_at


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


class MachineController:
    def __init__(
        self,
        presenter: BasePresenter,
        machine_service: IMachineService,
        order_service: IOrderService,
        payment_service: IPaymentService,
        machine_id: str,
    ):
        self._presenter = presenter
        self._machine_service = machine_service
        self._order_service = order_service
        self._payment_service = payment_service
        self._machine_id = machine_id

    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        try:
            output: ChooseProductOutputDTO = await self._machine_service.choose_product(
                ChooseProductInputDTO(input_dto.product_code, self._machine_id)
            )
            return self._presenter.execute(output)
        except Exception as error:
            return self._presenter.execute(ChooseProductErrorOutputControllerDTO(str(error)))

    async def pay_for_product(self, input_dto: PayForProductInputControllerDTO) -> Any:
        try:
            add_coins_output = await self._machine_service.add_coins(
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
            create_order_output: CreateOrderOutputDTO = await self._order_service.create(
                CreateOrderInputDTO(self._machine_id, input_dto.product_id, input_dto.product_qty)
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
            await self._machine_service.allow_dispense(AllowDispenseInputDTO(self._machine_id))
            await self._machine_service.deliver_product(
                DeliverProductInputDTO(self._machine_id, input_dto.product_id, input_dto.product_qty)
            )
            await self._machine_service.finish_dispense(FinishDispenseInputDTO(self._machine_id))
            return self._presenter.execute(add_coins_output)
        except Exception as error:
            return self._presenter.execute(
                PayForProductErrorOutputControllerDTO(
                    str(error),
                    input_dto.coin_01_qty,
                    input_dto.coin_05_qty,
                    input_dto.coin_10_qty,
                    input_dto.coin_25_qty,
                    input_dto.coin_50_qty,
                    input_dto.coin_100_qty,
                )
            )
