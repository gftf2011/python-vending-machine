from datetime import datetime

import pytest

from src.domain.entities.payment import CashPaymentEntity, PaymentEntity, PaymentType

from src.domain.exceptions.not_enough_cash_tendered import NotEnoughCashTenderedException

class Test_Payment_Entity:
    """Test class to test the cash entity"""
    def test_should_create_sut(self):
        """Function to test if the software component will create default payment"""
        payment_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        order_id: str = "b9651752-6c44-4578-bdb6-883d703cbff6"
        payment_type: PaymentType = PaymentType.CASH
        amount: int = 1
        payment_date: datetime = datetime.now()
        sut: PaymentEntity = PaymentEntity(payment_id, order_id, payment_type, amount, payment_date)
        assert sut.id.value == payment_id
        assert sut.order_id.value == order_id
        assert sut.type == payment_type
        assert sut.payment_date == payment_date
        assert sut.amount == amount 

class Test_Cash_Payment_Entity:
    """Test class to test the cash payment entity"""
    def test_should_raise_exception_by_using_constructor(self):
        """Function to test if the software component will raise an exception if calls the constructor"""
        payment_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        order_id: str = "b9651752-6c44-4578-bdb6-883d703cbff6"
        payment_type: PaymentType = PaymentType.CASH
        amount: int = 1
        payment_date: datetime = datetime.now()
        cash_tendered: int = 1
        with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
            CashPaymentEntity(payment_id, order_id, payment_type, amount, payment_date, cash_tendered)

    def test_should_raise_exception_if_cash_tendered_is_not_enough(self):
        """Function to test if the software component will raise if there is not enough cash"""
        payment_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        order_id: str = "b9651752-6c44-4578-bdb6-883d703cbff6"
        amount: int = 1
        cash_tendered: int = 0
        with pytest.raises(NotEnoughCashTenderedException):
            CashPaymentEntity.create(payment_id, order_id, amount, cash_tendered)

    def test_should_create_sut(self):
        """Function to test if the software component will create cash payment"""
        payment_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        order_id: str = "b9651752-6c44-4578-bdb6-883d703cbff6"
        amount: int = 1
        cash_tendered: int = 1
        sut = CashPaymentEntity.create(payment_id, order_id, amount, cash_tendered)
        assert sut.cash_payment_id.value == sut.id.value
        assert sut.cash_tendered == cash_tendered
        assert sut.change == cash_tendered - amount
