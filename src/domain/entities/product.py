from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.exceptions.invalid_products_qty import InvalidProductsQtyException
from src.domain.exceptions.invalid_products_price import InvalidProductsPriceException


class ProductEntity:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, id: str, name: str, qty: int, code: str, unit_price: int):
        self._id: UUIDValueObject = UUIDValueObject.create(id)
        self._name: str = name
        self._qty: int = qty
        self._code: str = code
        self._unit_price: int = unit_price

    @classmethod
    def create(cls, id: str, name: str, qty: int, code: str, unit_price: int) -> Self:
        if qty < 0:
            raise InvalidProductsQtyException()
        if unit_price < 0:
            raise InvalidProductsPriceException()
        instance = super().__new__(cls)
        instance.__init__(id, name, qty, code, unit_price)
        return instance

    @property
    def id(self) -> UUIDValueObject:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def qty(self) -> int:
        return self._qty

    @property
    def code(self) -> str:
        return self._code

    @property
    def unit_price(self) -> int:
        return self._unit_price

    def increase_qty(self) -> None:
        self._qty += 1

    def reduce_qty(self) -> None:
        if self._qty <= 0:
            raise InvalidProductsQtyException()
        self._qty -= 1
