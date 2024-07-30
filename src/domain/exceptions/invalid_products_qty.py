class InvalidProductsQtyException(Exception):
    def __init__(self):
        message = 'quantity of products can not be negative'
        super().__init__(message)
