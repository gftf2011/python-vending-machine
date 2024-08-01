from abc import ABC, abstractmethod


class CreateOrderInputDTO:
    def __init__(self, machine_id: str, product_id: str, product_qty: int):
        self.product_id = product_id
        self.machine_id = machine_id
        self.product_qty = product_qty


class CreateOrderOutputDTO:
    def __init__(self, order_id: str):
        self.order_id = order_id


class DeliverOrderInputDTO:
    def __init__(self, order_id: str):
        self.order_id = order_id


class IOrderService(ABC):
    @abstractmethod
    async def create(self, input_dto: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        """Function used to create an order"""
        raise NotImplementedError

    @abstractmethod
    async def deliver_order(self, input_dto: DeliverOrderInputDTO) -> None:
        """Function used to update order to DELIVERED status"""
        raise NotImplementedError
