import pytest

from src.domain.value_objects.email import EmailValueObject
from src.domain.exceptions.invalid_email import InvalidEmailException

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        EmailValueObject("test@mail.com")

def test_should_raise_exception_if_email_is_invalid():
    email: str = "test@.com"
    with pytest.raises(InvalidEmailException, match='email is invalid: ' + email):
        EmailValueObject.create(email)

def test_should_get_value():
    email: str = "test@mail.com"
    sut = EmailValueObject.create(email)
    assert sut.get_value() == email