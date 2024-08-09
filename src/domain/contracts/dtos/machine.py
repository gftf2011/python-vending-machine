from typing import Dict, Union

from src.domain.contracts.dtos.base import BaseOutput

ChooseProductOutputDictType = Union[
    Dict["product_id", str], Dict["product_price", int], Dict["product_name", str]
]

AddCoinsOutputDictType = Union[
    Dict["coin_01_qty", int],
    Dict["coin_05_qty", int],
    Dict["coin_10_qty", int],
    Dict["coin_25_qty", int],
    Dict["coin_50_qty", int],
    Dict["coin_100_qty", int],
]

DeliverProductOutputDictType = Union[Dict["product_id", str], Dict["product_code", str]]


class ChooseProductInputDTO:
    def __init__(self, product_code: str, machine_id: str):
        self.product_code = product_code
        self.machine_id = machine_id


class ChooseProductOutputDTO(BaseOutput):
    def __init__(self, product_id: str, product_price: int, product_name: str):
        self.product_id = product_id
        self.product_price = product_price
        self.product_name = product_name

    def to_dict(self) -> ChooseProductOutputDictType:
        return {
            "product_id": self.product_id,
            "product_price": self.product_price,
            "product_name": self.product_name,
        }


class AddCoinsInputDTO:
    def __init__(
        self,
        machine_id: str,
        product_id: str,
        coin_01_qty: int,
        coin_05_qty: int,
        coin_10_qty: int,
        coin_25_qty: int,
        coin_50_qty: int,
        coin_100_qty: int,
    ):
        self.machine_id = machine_id
        self.product_id = product_id
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty


class AddCoinsOutputDTO(BaseOutput):
    def __init__(
        self,
        coin_01_qty: int,
        coin_05_qty: int,
        coin_10_qty: int,
        coin_25_qty: int,
        coin_50_qty: int,
        coin_100_qty: int,
        amount_paid: int,
    ):
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty
        self.amount_paid = amount_paid

    def to_dict(self) -> AddCoinsOutputDictType:
        return {
            "coin_01_qty": self.coin_01_qty,
            "coin_05_qty": self.coin_05_qty,
            "coin_10_qty": self.coin_10_qty,
            "coin_25_qty": self.coin_25_qty,
            "coin_50_qty": self.coin_50_qty,
            "coin_100_qty": self.coin_100_qty,
            "amount_paid": self.amount_paid,
        }


class AllowDispenseInputDTO:
    def __init__(self, machine_id: str):
        self.machine_id = machine_id


class DeliverProductInputDTO:
    def __init__(self, machine_id: str, product_id: str, product_qty: int):
        self.machine_id = machine_id
        self.product_id = product_id
        self.product_qty = product_qty


class DeliverProductOutputDTO(BaseOutput):
    def __init__(self, product_id: str, product_code: str):
        self.product_id = product_id
        self.product_code = product_code

    def to_dict(self) -> DeliverProductOutputDictType:
        return {
            "product_id": self.product_id,
            "product_code": self.product_code,
        }


class FinishDispenseInputDTO:
    def __init__(self, machine_id: str):
        self.machine_id = machine_id
