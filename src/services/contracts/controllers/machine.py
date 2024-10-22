from typing import Any
from abc import ABC, abstractmethod

from src.domain.entities.payment import PaymentType


class ChooseProductInputControllerDTO:
    def __init__(self, product_code: str, machine_id: str):
        self.product_code = product_code
        self.machine_id = machine_id


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


class IMachineController(ABC):
    @abstractmethod
    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def pay_for_product(self, input_dto: PayForProductInputControllerDTO) -> Any:
        raise NotImplementedError
