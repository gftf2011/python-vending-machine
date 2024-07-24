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

class IMachineService(ABC):
    @abstractmethod
    async def choose_product(self, input: ChooseProductInputDTO) -> ChooseProductOutputDTO:
        raise NotImplementedError