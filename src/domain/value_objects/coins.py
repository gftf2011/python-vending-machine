from enum import IntEnum
from typing import Self

from src.domain.exceptions.invalid_coins_qty import InvalidCoinsQtyException


class CoinTypes(IntEnum):
    COIN_01 = 1
    COIN_05 = 5
    COIN_10 = 10
    COIN_25 = 25
    COIN_50 = 50
    COIN_100 = 100


class CoinsValueObject:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, value: CoinTypes, qty: int):
        self._value = value
        self._qty = qty

    @staticmethod
    def _validate(qty: int) -> None:
        if qty < 0:
            raise InvalidCoinsQtyException()

    @classmethod
    def create(cls, value: CoinTypes, qty: int) -> Self:
        CoinsValueObject._validate(qty)
        instance = super().__new__(cls)
        instance.__init__(value, qty)
        return instance

    @property
    def value(self) -> CoinTypes:
        return self._value

    @property
    def qty(self) -> int:
        return self._qty

    def increase_qty(self) -> None:
        self._qty += 1

    def reduce_qty(self) -> None:
        if self._qty <= 0:
            raise InvalidCoinsQtyException()
        self._qty -= 1
