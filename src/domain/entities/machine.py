from enum import Enum
from typing import Self

from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.value_objects.coins import CoinsValueObject, CoinTypes

from src.domain.exceptions.no_change_available import NoChangeAvailableException

class CoinsChange:
    def __init__(self, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int):
        self.coin_01_qty: int = coin_01_qty
        self.coin_05_qty: int = coin_05_qty
        self.coin_10_qty: int = coin_10_qty
        self.coin_25_qty: int = coin_25_qty
        self.coin_50_qty: int = coin_50_qty
        self.coin_100_qty: int = coin_100_qty
        

class MachineState(Enum):
    READY = 'READY'
    DISPENSING = 'DISPENSING'

class MachineEntity:
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

    def get_amount_out_of_coins(self, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int) -> int:
        amount: int = 0

        while coin_01_qty > 0:
            amount += 1
            coin_01_qty -= 1

        while coin_05_qty > 0:
            amount += 5
            coin_05_qty -= 1

        while coin_10_qty > 0:
            amount += 10
            coin_10_qty -= 1

        while coin_25_qty > 0:
            amount += 25
            coin_25_qty -= 1

        while coin_50_qty > 0:
            amount += 50
            coin_50_qty -= 1

        while coin_100_qty > 0:
            amount += 100
            coin_100_qty -= 1

        return amount

    def get_coins_from_change(self, change: int) -> CoinsChange:
        coin_100: int = 0
        while self.__coin_100.get_qty() > 0 and self.__coin_100.get_value() <= change:
            self.__coin_100.reduce_qty()
            change -= self.__coin_100.get_value()
            coin_100 += 1

        coin_50: int = 0
        while self.__coin_50.get_qty() > 0 and self.__coin_50.get_value() <= change:
            self.__coin_50.reduce_qty()
            change -= self.__coin_50.get_value()
            coin_50 += 1

        coin_25: int = 0
        while self.__coin_25.get_qty() > 0 and self.__coin_25.get_value() <= change:
            self.__coin_25.reduce_qty()
            change -= self.__coin_25.get_value()
            coin_25 += 1

        coin_10: int = 0
        while self.__coin_10.get_qty() > 0 and self.__coin_10.get_value() <= change:
            self.__coin_10.reduce_qty()
            change -= self.__coin_10.get_value()
            coin_10 += 1
        
        coin_05: int = 0
        while self.__coin_05.get_qty() > 0 and self.__coin_05.get_value() <= change:
            self.__coin_05.reduce_qty()
            change -= self.__coin_05.get_value()
            coin_05 += 1

        coin_01: int = 0
        while self.__coin_01.get_qty() > 0 and self.__coin_01.get_value() <= change:
            self.__coin_01.reduce_qty()
            change -= self.__coin_01.get_value()
            coin_01 += 1

        if change != 0:
            raise NoChangeAvailableException()

        return CoinsChange(coin_01, coin_05, coin_10, coin_25, coin_50, coin_100)

    def add_coins(self, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int) -> None:
        while coin_01_qty > 0:
            self.__coin_01.increase_qty()
            coin_01_qty -= 1

        while coin_05_qty > 0:
            self.__coin_05.increase_qty()
            coin_05_qty -= 1

        while coin_10_qty > 0:
            self.__coin_10.increase_qty()
            coin_10_qty -= 1

        while coin_25_qty > 0:
            self.__coin_25.increase_qty()
            coin_25_qty -= 1

        while coin_50_qty > 0:
            self.__coin_50.increase_qty()
            coin_50_qty -= 1

        while coin_100_qty > 0:
            self.__coin_100.increase_qty()
            coin_100_qty -= 1

    def subtract_coins(self, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int) -> None:
        while coin_01_qty > 0:
            self.__coin_01.reduce_qty()
            coin_01_qty -= 1

        while coin_05_qty > 0:
            self.__coin_05.reduce_qty()
            coin_05_qty -= 1

        while coin_10_qty > 0:
            self.__coin_10.reduce_qty()
            coin_10_qty -= 1

        while coin_25_qty > 0:
            self.__coin_25.reduce_qty()
            coin_25_qty -= 1

        while coin_50_qty > 0:
            self.__coin_50.reduce_qty()
            coin_50_qty -= 1

        while coin_100_qty > 0:
            self.__coin_100.reduce_qty()
            coin_100_qty -= 1