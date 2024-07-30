class IncorrectNegativeChangeException(Exception):
    def __init__(self):
        message = "change can not be negative"
        super().__init__(message)
