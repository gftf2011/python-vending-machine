from src.domain.entities.order import OrderEntity
from src.domain.entities.payment import CashPaymentEntity, PaymentEntity, PaymentType

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.order import IOrderRepository
from src.domain.repositories.payment import IPaymentRepository

from src.domain.contracts.services.payment import IPaymentService, PayForProductInputDTO, PayForProductOutputDTO

from src.services.exceptions.order_does_not_exist import OrderDoesNotExistException
from src.services.exceptions.not_enough_for_payment import NotEnoughForPaymentException
from src.services.exceptions.invalid_payment_type import InvalidPaymentTypeException

class PaymentService(IPaymentService):
    def __init__(self, order_repo: IOrderRepository, payment_repo: IPaymentRepository):
        self.__order_repo: IOrderRepository = order_repo
        self.__payment_repo: IPaymentRepository = payment_repo

    async def pay_for_product(self, input: PayForProductInputDTO) -> PayForProductOutputDTO:
        order_found: OrderEntity = await self.__order_repo.find_by_id(UUIDValueObject.create(input.order_id))
        if not order_found:
            raise OrderDoesNotExistException(input.order_id)

        if order_found.get_total_amount() > input.amount_paid:
            raise NotEnoughForPaymentException(input.amount_paid, order_found.get_id().value)

        payment: PaymentEntity = None

        payment_id: str = UUIDValueObject.create_new().value

        if input.payment_type == PaymentType.CASH:
            payment = CashPaymentEntity.create(payment_id, input.order_id, order_found.get_total_amount(), input.amount_paid)

        if payment == None:
            raise InvalidPaymentTypeException(str(input.payment_type))

        change: int = payment.change

        await self.__payment_repo.save(payment)

        return PayForProductOutputDTO(payment_id, change)
