import pytest

from src.domain.value_objects.email import EmailValueObject
from src.domain.exceptions.invalid_email import InvalidEmailException

def test_should_raise_exception_by_using_constructor():
    """Function to test if the software component will raise an exception if calls the constructor"""
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        EmailValueObject("test@mail.com")

def test_should_raise_exception_if_email_is_invalid():
    """Function to test if Email will raise exception when try to create software component with an invalid value"""
    email: str = "test@.com"
    with pytest.raises(InvalidEmailException, match='email is invalid: ' + email):
        EmailValueObject.create(email)

def test_should_get_value():
    """Function to test the entity value"""
    email: str = "test@mail.com"
    sut = EmailValueObject.create(email)
    assert sut.value == email
