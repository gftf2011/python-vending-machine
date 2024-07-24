class UnavailableProductException(Exception):
    def __init__(self, id: str):
        message = 'product - "' + id + '" - is not available in the machine'
        super().__init__(message)