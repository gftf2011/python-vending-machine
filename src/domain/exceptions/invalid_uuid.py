class InvalidUUIDException(Exception):
    def __init__(self, id_value: str):
        message = 'id is invalid: ' + id_value
        super().__init__(message)
