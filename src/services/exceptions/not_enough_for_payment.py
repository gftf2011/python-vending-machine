class NotEnoughForPaymentException(Exception):
    def __init__(self, amount_paid: int, order_id: str):
        message = (
            "payment of - " + str(amount_paid) + " - not enough for order - " + order_id
        )
        super().__init__(message)
