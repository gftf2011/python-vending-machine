class InvalidOrderItemProductQtyException(Exception):
    def __init__(self):
        message = 'quantity of products in order item can not be less than 1'
        super().__init__(message)