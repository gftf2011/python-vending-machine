class InvalidPaymentTypeException(Exception):
    def __init__(self, payment_type: str):
        message = "payment type - " + payment_type + " - does not exists"
        super().__init__(message)