import uuid

import pytest

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.exceptions.invalid_uuid import InvalidUUIDException


def test_should_raise_exception_by_using_constructor():
    """Function to test if the software component will raise an exception if calls the constructor"""
    with pytest.raises(
        Exception,
        match="Use the 'create' OR 'create_new' methods to create an instance of this class.",
    ):
        UUIDValueObject("b9651752-6c44-4578-bdb6-883d703cbff5")


def test_should_raise_exception_if_id_is_invalid():
    """Function to test if UUID will raise exception when try to create software component with an invalid value"""
    id_value: str = "wrong-uuid"
    with pytest.raises(InvalidUUIDException, match="id is invalid: " + id_value):
        UUIDValueObject.create(id_value)


def test_should_create():
    """Function to test if an UUID is created with a predefined value"""
    id_value: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
    sut = UUIDValueObject.create(id_value)
    assert sut.value == id_value


def test_should_create_new():
    """Function to test if an UUID is created"""
    sut = UUIDValueObject.create_new()
    assert sut.value is not None


def test_should_convert_to_UUID():
    """Function to test if an UUID is created"""
    sut = UUIDValueObject.create_new()
    assert isinstance(sut.convert_value_to_UUID(), uuid.UUID) is True
