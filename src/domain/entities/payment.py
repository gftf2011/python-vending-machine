from enum import Enum
from datetime import datetime
from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.exceptions.not_enough_cash_tendered import (
    NotEnoughCashTenderedException,
)


class PaymentType(Enum):
    CASH = "CASH"


class PaymentEntity:
    def __init__(
        self,
        id: str,
        order_id: str,
        type: PaymentType,
        amount: int,
        payment_date: datetime,
    ):
        self._id: UUIDValueObject = UUIDValueObject.create(id)
        self._order_id: UUIDValueObject = UUIDValueObject.create(order_id)
        self._type: PaymentType = type
        self._amount: int = amount
        self._payment_date: datetime = payment_date

    @property
    def id(self) -> UUIDValueObject:
        return self._id

    @property
    def order_id(self) -> UUIDValueObject:
        return self._order_id

    @property
    def type(self) -> PaymentType:
        return self._type

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def payment_date(self) -> datetime:
        return self._payment_date


class CashPaymentEntity(PaymentEntity):
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(
        self,
        id: str,
        order_id: str,
        type: PaymentType,
        amount: int,
        payment_date: datetime,
        cash_tendered: int,
    ):
        super().__init__(id, order_id, type, amount, payment_date)
        self._cash_payment_id: UUIDValueObject = UUIDValueObject.create(id)
        self._cash_tendered: int = cash_tendered

    @classmethod
    def create(cls, id: str, order_id: str, amount: int, cash_tendered: int) -> Self:
        instance = super().__new__(cls)
        if cash_tendered < amount:
            raise NotEnoughCashTenderedException(amount, cash_tendered)
        instance.__init__(
            id, order_id, PaymentType.CASH, amount, datetime.now(), cash_tendered
        )
        return instance

    @property
    def cash_payment_id(self) -> UUIDValueObject:
        return self._cash_payment_id

    @property
    def cash_tendered(self) -> int:
        return self._cash_tendered

    @property
    def change(self) -> int:
        change: int = self._cash_tendered - self._amount
        return change
