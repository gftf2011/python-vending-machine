from datetime import datetime
from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.product import ProductEntity

from src.domain.exceptions.invalid_order_item_product_qty import InvalidOrderItemProductQtyException

class OrderItemEntity:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' OR 'create_new' methods to create an instance of this class.")

    def __init__(self, id: str, product: ProductEntity, price: int, qty: int, created_at: datetime):
        self._id: UUIDValueObject = UUIDValueObject.create(id)
        self._product: ProductEntity = product
        self._price: int = price
        self._qty: int = qty
        self._created_at: datetime = created_at

    @classmethod
    def create(cls, id: str, product: ProductEntity, created_at: datetime) -> Self:
        instance = super().__new__(cls)
        price: int = product.get_unit_price()
        qty: int = product.get_qty()

        if qty <= 0:
            raise InvalidOrderItemProductQtyException()

        instance.__init__(id, product, price, qty, created_at)
        return instance

    @classmethod
    def create_new(cls, id: str, product: ProductEntity) -> Self:
        instance = super().__new__(cls)
        price: int = product.get_unit_price()
        qty: int = product.get_qty()

        if qty <= 0:
            raise InvalidOrderItemProductQtyException()

        created_at: datetime = datetime.now()
        instance.__init__(id, product, price, qty, created_at)
        return instance

    @property
    def id(self) -> UUIDValueObject:
        return self._id

    @property
    def product(self) -> ProductEntity:
        return self._product

    @property
    def price(self) -> int:
        return self._price

    @property
    def qty(self) -> int:
        return self._qty

    @property
    def created_at(self) -> datetime:
        return self._created_at