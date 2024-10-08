from typing import Dict, Union

from src.domain.contracts.dtos.base import BaseOutput

from src.domain.entities.payment import PaymentType

PayForProductOutputDictType = Union[Dict["payment_id", str], Dict["change", int]]


class PayForProductInputDTO:
    def __init__(
        self, order_id: str, machine_id: str, amount_paid: int, payment_type: PaymentType, order_created_at: str
    ):
        self.order_id = order_id
        self.machine_id = machine_id
        self.order_created_at = order_created_at
        self.amount_paid = amount_paid
        self.payment_type = payment_type


class PayForProductOutputDTO(BaseOutput):
    def __init__(self, payment_id: str, change: int):
        self.change = change
        self.payment_id = payment_id

    def to_dict(self) -> PayForProductOutputDictType:
        return {"payment_id": self.payment_id, "change": self.change}
