class InvalidUUIDException(Exception):
    def __init__(self, id: str):
        message = 'id is invalid: ' + id
        super().__init__(message)