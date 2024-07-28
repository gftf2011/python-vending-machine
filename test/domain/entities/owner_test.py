import pytest

from src.domain.entities.owner import OwnerEntity
from src.domain.exceptions.invalid_email import InvalidEmailException

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        OwnerEntity("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")

def test_should_get_id():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    assert owner.id.value == "b9651752-6c44-4578-bdb6-883d703cbff5"

def test_should_get_full_name():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    assert owner.full_name == "Sebastião Maia"

def test_should_get_email():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    assert owner.email.value == "test@mail.com"
