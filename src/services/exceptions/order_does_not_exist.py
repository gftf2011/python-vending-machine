class OrderDoesNotExistException(Exception):
    def __init__(self, id: str):
        message = "order - " + id + " - does not exists"
        super().__init__(message)