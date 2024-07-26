class InvalidOrderStatusChangeException(Exception):
    def __init__(self, id: str):
        message = 'order - ' + id + ' - STATUS can not be changed'
        super().__init__(message)