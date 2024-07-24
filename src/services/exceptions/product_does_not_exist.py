class ProductDoesNotExistException(Exception):
    def __init__(self):
        message = "product does not exists"
        super().__init__(message)