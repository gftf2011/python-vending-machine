from abc import ABC, abstractmethod

class CreateOrderInputDTO:
    def __init__(self, machine_id: str, product_id: str, product_qty: int):
        self.product_id = product_id
        self.machine_id = machine_id
        self.product_qty = product_qty

class CreateOrderOutputDTO:
    def __init__(self, order_id: str):
        self.order_id = order_id

class IOrderService(ABC):
    @abstractmethod
    async def create(self, input_dto: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        raise NotImplementedError
