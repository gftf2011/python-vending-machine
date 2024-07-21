from typing import Self

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.value_objects.email import EmailValueObject

class OwnerEntity:
    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'create' method to create an instance of this class.")

    def __init__(self, id: str, full_name: str, email: str):
        self.__id: UUIDValueObject = UUIDValueObject.create(id)
        self.__full_name = full_name
        self.__email: EmailValueObject = EmailValueObject.create(email)

    @classmethod
    def create(cls, id: str, full_name: str, email: str) -> Self:
        instance = super().__new__(cls)
        instance.__init__(id, full_name, email)
        return instance
    
    def get_id(self) -> UUIDValueObject:
        return self.__id

    def get_full_name(self) -> str:
        return self.__full_name
    
    def get_email(self) -> EmailValueObject:
        return self.__email