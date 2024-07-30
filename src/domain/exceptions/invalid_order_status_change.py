class InvalidOrderStatusChangeException(Exception):
    def __init__(self, id_value: str):
        message = "order - " + id_value + " - STATUS can not be changed"
        super().__init__(message)
