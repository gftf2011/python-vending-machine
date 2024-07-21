from enum import Enum
from typing import Self

from src.domain.exceptions.invalid_coins_qty import InvalidCoinsQty

class CoinTypes(Enum):
    COIN_01 = 1
    COIN_05 = 5
    COIN_10 = 10
    COIN_25 = 25
    COIN_50 = 50
    COIN_100 = 100

class CoinsValueObject:
    __value: CoinTypes
    __qty: int

    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, value: CoinTypes, qty: int):
        CoinsValueObject.__value = value
        CoinsValueObject.__qty = qty

    @staticmethod
    def __validate(qty: int) -> None:
        if qty < 0:
            raise InvalidCoinsQty()
    
    @classmethod
    def create(cls, value: CoinTypes, qty: int) -> Self:
        CoinsValueObject.__validate(qty)
        instance = super().__new__(cls)
        instance.__init__(value, qty)
        return instance
    
    @classmethod
    def get_value(cls) -> CoinTypes:
        return cls.__value

    @classmethod
    def get_qty(cls) -> int:
        return cls.__qty
    
    def increase_qty(self) -> None:
        CoinsValueObject.__qty += 1
    
    def reduce_qty(self) -> None:
        if CoinsValueObject.__qty <= 0:
            raise InvalidCoinsQty()
        CoinsValueObject.__qty -= 1
