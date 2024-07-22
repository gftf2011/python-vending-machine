import uuid

from typing import Self

from src.domain.exceptions.invalid_uuid import InvalidUUIDException

class UUIDValueObject:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, value: str):
        self.__value = value
    
    @staticmethod
    def __validate(id: str) -> None:
        try:
            uuid.UUID(id, version=4)
            return True
        except ValueError:
            raise InvalidUUIDException(id)
    
    @classmethod
    def create(cls, id: str) -> Self:
        UUIDValueObject.__validate(id)
        instance = super().__new__(cls)
        instance.__init__(id)
        return instance

    def get_value(self) -> str:
        return self.__value