from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.exceptions.invalid_products_qty import InvalidProductsQtyException
from src.domain.exceptions.invalid_products_price import InvalidProductsPriceException

class ProductEntity:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, id: str, name: str, qty: int, code: str, unit_price: int):
        self.__id: UUIDValueObject = UUIDValueObject.create(id)
        self.__name: str = name
        self.__qty: int = qty
        self.__code: str = code
        self.__unit_price: int = unit_price
    
    @classmethod
    def create(cls, id: str, name: str, qty: int, code: str, unit_price: int) -> Self:
        if qty < 0:
            raise InvalidProductsQtyException()
        if unit_price < 0:
            raise InvalidProductsPriceException()
        instance = super().__new__(cls)
        instance.__init__(id, name, qty, code, unit_price)
        return instance
    
    def get_id(self) -> UUIDValueObject:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_qty(self) -> int:
        return self.__qty

    def get_code(self) -> str:
        return self.__code
    
    def get_unit_price(self) -> int:
        return self.__unit_price

    def increase_qty(self) -> None:
        self.__qty += 1
    
    def reduce_qty(self) -> None:
        if self.__qty <= 0:
            raise InvalidProductsQtyException()
        self.__qty -= 1