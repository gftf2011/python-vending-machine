from abc import ABC, abstractmethod

from src.domain.entities.payment import PaymentType

class PayForProductInputDTO:
    def __init__(self, order_id: str, amount_paid: int, payment_type: PaymentType):
        self.order_id = order_id
        self.amount_paid = amount_paid
        self.payment_type = payment_type

class PayForProductOutputDTO:
    def __init__(self, payment_id: str, change: int):
        self.change = change
        self.payment_id = payment_id

class IPaymentService(ABC):
    @abstractmethod
    async def pay_for_product(self, input_dto: PayForProductInputDTO) -> PayForProductOutputDTO:
        """Function used to create the payment for chosen product"""
        raise NotImplementedError
