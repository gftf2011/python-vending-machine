from typing import Dict, Union

from src.domain.contracts.dtos.base import BaseOutput

CreateOrderOutputDictType = Union[Dict["order_id", str]]


class CreateOrderInputDTO:
    def __init__(self, machine_id: str, product_id: str, product_qty: int):
        self.product_id = product_id
        self.machine_id = machine_id
        self.product_qty = product_qty


class CreateOrderOutputDTO(BaseOutput):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def to_dict(self) -> CreateOrderOutputDictType:
        return {"order_id": self.order_id}


class DeliverOrderInputDTO:
    def __init__(self, order_id: str, machine_id: str, order_created_at: str):
        self.order_id = order_id
        self.machine_id = machine_id
        self.order_created_at = order_created_at
