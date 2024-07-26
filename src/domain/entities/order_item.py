from datetime import datetime
from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.product import ProductEntity

class OrderItemEntity:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' OR 'create_new' methods to create an instance of this class.")

    def __init__(self, id: str, product: ProductEntity, price: int, qty: int, created_at: datetime):
        self.__id: UUIDValueObject = UUIDValueObject.create(id)
        self.__product: ProductEntity = product
        self.__price: int = price
        self.__qty: int = qty
        self.__created_at: datetime = created_at

    @classmethod
    def create(cls, id: str, product: ProductEntity, created_at: datetime) -> Self:
        instance = super().__new__(cls)
        price: int = product.get_unit_price()
        qty: int = product.get_qty()
        instance.__init__(id, product, price, qty, created_at)
        return instance

    @classmethod
    def create_new(cls, id: str, product: ProductEntity) -> Self:
        instance = super().__new__(cls)
        price: int = product.get_unit_price()
        qty: int = product.get_qty()
        created_at: datetime = datetime.now()
        instance.__init__(id, product, price, qty, created_at)
        return instance
    
    def get_id(self) -> UUIDValueObject:
        return self.__id

    def get_product(self) -> ProductEntity:
        return self.__product
    
    def get_price(self) -> int:
        return self.__price

    def get_qty(self) -> int:
        return self.__qty

    def get_created_at(self) -> datetime:
        return self.__created_at