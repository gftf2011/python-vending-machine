import pytest

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.exceptions.invalid_uuid import InvalidUUIDException

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' OR 'create_new' methods to create an instance of this class."):
        UUIDValueObject("b9651752-6c44-4578-bdb6-883d703cbff5")

def test_should_raise_exception_if_id_is_invalid():
    id: str = "wrong-uuid"
    with pytest.raises(InvalidUUIDException, match='id is invalid: ' + id):
        UUIDValueObject.create(id)

def test_should_create():
    id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
    sut = UUIDValueObject.create(id)
    assert sut.get_value() == id

def test_should_create_new():
    sut = UUIDValueObject.create_new()
    assert sut.get_value() != None
