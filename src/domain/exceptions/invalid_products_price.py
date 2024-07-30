class InvalidProductsPriceException(Exception):
    def __init__(self):
        message = "price of products can not be negative"
        super().__init__(message)
