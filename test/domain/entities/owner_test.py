import pytest

from src.domain.entities.owner import OwnerEntity
from src.domain.exceptions.invalid_email import InvalidEmailException

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        OwnerEntity("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")

def test_should_get_id():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    assert owner.get_id() == "b9651752-6c44-4578-bdb6-883d703cbff5"

def test_should_get_full_name():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    assert owner.get_full_name() == "Sebastião Maia"

def test_should_get_email():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    assert owner.get_email() == "test@mail.com"

def test_throw_exception_if_email_is_invalid():
    email: str = "test@.com"
    with pytest.raises(InvalidEmailException, match='email is invalid: ' + email):
        OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", email)