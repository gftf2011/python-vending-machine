from enum import Enum
from typing import Self

from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.value_objects.coins import CoinsValueObject, CoinTypes

class MachineState(Enum):
    READY = 'READY'
    DISPENSING = 'DISPENSING'

class MachineAggregate:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, id: str, owner: OwnerEntity, state: MachineState, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int, products: list[ProductEntity]):
        self.__id: UUIDValueObject = UUIDValueObject.create(id)
        self.__owner: OwnerEntity = owner
        self.__state = state
        self.__coin_01: CoinsValueObject = CoinsValueObject.create(CoinTypes.COIN_01, coin_01_qty)
        self.__coin_05: CoinsValueObject = CoinsValueObject.create(CoinTypes.COIN_05, coin_05_qty)
        self.__coin_10: CoinsValueObject = CoinsValueObject.create(CoinTypes.COIN_10, coin_10_qty)
        self.__coin_25: CoinsValueObject = CoinsValueObject.create(CoinTypes.COIN_25, coin_25_qty)
        self.__coin_50: CoinsValueObject = CoinsValueObject.create(CoinTypes.COIN_50, coin_50_qty)
        self.__coin_100: CoinsValueObject = CoinsValueObject.create(CoinTypes.COIN_100, coin_100_qty)
        self.__products: list[ProductEntity] = products
    
    @classmethod
    def create(cls, id: str, owner: OwnerEntity, state: MachineState, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int, products: list[ProductEntity]) -> Self:
        instance = super().__new__(cls)
        instance.__init__(id, owner, state, coin_01_qty, coin_05_qty, coin_10_qty, coin_25_qty, coin_50_qty, coin_100_qty, products)
        return instance
    
    def get_id(self) -> UUIDValueObject:
        return self.__id

    def get_state(self) -> MachineState:
        return self.__state
    
    def get_coin_01(self) -> CoinsValueObject:
        return self.__coin_01

    def get_coin_05(self) -> CoinsValueObject:
        return self.__coin_05
    
    def get_coin_10(self) -> CoinsValueObject:
        return self.__coin_10
    
    def get_coin_25(self) -> CoinsValueObject:
        return self.__coin_25
    
    def get_coin_50(self) -> CoinsValueObject:
        return self.__coin_50
    
    def get_coin_100(self) -> CoinsValueObject:
        return self.__coin_100
    
    def get_owner(self) -> OwnerEntity:
        return self.__owner

    def get_products(self) -> list[ProductEntity]:
        return self.__products

    def finish_dispense_product(self) -> None:
        self.__state = MachineState.READY
    
    def start_dispense_product(self) -> None:
        self.__state = MachineState.DISPENSING
