class NoChangeAvailableException(Exception):
    def __init__(self):
        message = 'not enough change in the machine'
        super().__init__(message)