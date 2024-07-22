from enum import Enum
from typing import Self

from src.domain.exceptions.invalid_coins_qty import InvalidCoinsQtyException

class CoinTypes(Enum):
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
        self.__value = value
        self.__qty = qty

    @staticmethod
    def __validate(qty: int) -> None:
        if qty < 0:
            raise InvalidCoinsQtyException()
    
    @classmethod
    def create(cls, value: CoinTypes, qty: int) -> Self:
        CoinsValueObject.__validate(qty)
        instance = super().__new__(cls)
        instance.__init__(value, qty)
        return instance

    def get_value(self) -> CoinTypes:
        return self.__value

    def get_qty(self) -> int:
        return self.__qty
    
    def increase_qty(self) -> None:
        self.__qty += 1
    
    def reduce_qty(self) -> None:
        if self.__qty <= 0:
            raise InvalidCoinsQtyException()
        self.__qty -= 1
