import uuid

from typing import Self

from src.domain.exceptions.invalid_uuid import InvalidUUIDException


class UUIDValueObject:
    def __new__(cls, *args, **kwargs):
        raise Exception(
            "Use the 'create' OR 'create_new' methods to create an instance of this class."
        )

    def __init__(self, value: str):
        self._value = value

    @staticmethod
    def _validate(id: str) -> None:
        try:
            uuid.UUID(id, version=4)
            return True
        except ValueError:
            raise InvalidUUIDException(id)

    @classmethod
    def create(cls, id: str) -> Self:
        UUIDValueObject._validate(id)
        instance = super().__new__(cls)
        instance.__init__(id)
        return instance

    @classmethod
    def create_new(cls) -> Self:
        instance = super().__new__(cls)
        instance.__init__(str(uuid.uuid4()))
        return instance

    @property
    def value(self) -> str:
        return self._value

    def convert_value_to_UUID(self) -> uuid.UUID:
        return uuid.UUID(self._value, version=4)
