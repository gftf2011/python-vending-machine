class InvalidCoinsQtyException(Exception):
    def __init__(self):
        message = 'quantity of coins can not be negative'
        super().__init__(message)