class InvalidEmailException(Exception):
    def __init__(self, email: str):
        message = 'email is invalid: ' + email
        super().__init__(message)
