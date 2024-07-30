from abc import ABC, abstractmethod

class ChooseProductInputDTO:
    def __init__(self, product_code: str, machine_id: str):
        self.product_code = product_code
        self.machine_id = machine_id


class ChooseProductOutputDTO:
    def __init__(self, product_id: str, product_price: int, product_name: str):
        self.product_id = product_id
        self.product_price = product_price
        self.product_name = product_name

class AddCoinsInputDTO:
    def __init__(self, machine_id: str, change: int, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int):
        self.machine_id = machine_id
        self.change = change
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty

class AddCoinsOutputDTO:
    def __init__(self, coin_01_qty: int, coin_05_qty: int, coin_10_qty: int, coin_25_qty: int, coin_50_qty: int, coin_100_qty: int):
        self.coin_01_qty = coin_01_qty
        self.coin_05_qty = coin_05_qty
        self.coin_10_qty = coin_10_qty
        self.coin_25_qty = coin_25_qty
        self.coin_50_qty = coin_50_qty
        self.coin_100_qty = coin_100_qty

class IMachineService(ABC):
    @abstractmethod
    async def choose_product(self, input_dto: ChooseProductInputDTO) -> ChooseProductOutputDTO:
        raise NotImplementedError

    @abstractmethod
    async def add_coins(self, input_dto: AddCoinsInputDTO) -> AddCoinsOutputDTO:
        raise NotImplementedError
