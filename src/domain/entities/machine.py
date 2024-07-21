from enum import Enum
from typing import Self

from src.domain.entities.owner import OwnerEntity

class MachineState(Enum):
    READY = 'READY'
    DISPENSING = 'DISPENSING'

class MachineAggregate:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, id: str, owner: OwnerEntity, state: MachineState, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int):
        self.__id = id
        self.__owner = owner
        self.__state = state
        self.__coin_01_qty = coin_01_qty
        self.__coin_05_qty = coin_05_qty
        self.__coin_10_qty = coin_10_qty
        self.__coin_25_qty = coin_25_qty
        self.__coin_50_qty = coin_50_qty
        self.__coin_100_qty = coin_100_qty
    
    @classmethod
    def create(cls, id: str, owner: OwnerEntity, state: MachineState, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int) -> Self:
        instance = super().__new__(cls)
        instance.__init__(id, owner, state, coin_01_qty, coin_05_qty, coin_10_qty, coin_25_qty, coin_50_qty, coin_100_qty)
        return instance
    
    def get_id(self) -> str:
        return self.__id

    def get_state(self) -> MachineState:
        return self.__state
    
    def get_coin_01_qty(self) -> int:
        return self.__coin_01_qty

    def get_coin_05_qty(self) -> int:
        return self.__coin_05_qty
    
    def get_coin_10_qty(self) -> int:
        return self.__coin_10_qty
    
    def get_coin_25_qty(self) -> int:
        return self.__coin_25_qty
    
    def get_coin_50_qty(self) -> int:
        return self.__coin_50_qty
    
    def get_coin_100_qty(self) -> int:
        return self.__coin_100_qty
    
    def get_owner(self) -> OwnerEntity:
        return self.__owner
    
    def finish_dispense_product(self) -> None:
        self.__state = MachineState.READY
    
    def start_dispense_product(self) -> None:
        self.__state = MachineState.DISPENSING