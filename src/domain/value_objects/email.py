import re

from typing import Self

from src.domain.exceptions.invalid_email import InvalidEmailException

class EmailValueObject:
    __value: str

    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, value: str):
        EmailValueObject.__value = value
    
    @staticmethod
    def __validate(email: str) -> None:
        regex = re.compile(r"^[-!#$%&'*+/0-9=?A-Z^_a-z`{|}~](\.?[-!#$%&'*+/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$")
        if bool(regex.match(email)) == False:
            raise InvalidEmailException(email)
    
    @classmethod
    def create(cls, email: str) -> Self:
        EmailValueObject.__validate(email)
        instance = super().__new__(cls)
        instance.__init__(email)
        return instance
    
    def get_value() -> str:
        return EmailValueObject.__value