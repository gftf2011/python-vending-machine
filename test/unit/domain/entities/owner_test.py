import pytest

from src.domain.entities.owner import OwnerEntity


def test_should_raise_exception_by_using_constructor():
    """Function to test if the software component will raise an exception if calls the constructor"""
    with pytest.raises(
        Exception, match="Use the 'create' method to create an instance of this class."
    ):
        OwnerEntity(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )


def test_should_get_id():
    """Function to test if id property is called"""
    owner = OwnerEntity.create(
        "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
    )
    assert owner.id.value == "b9651752-6c44-4578-bdb6-883d703cbff5"


def test_should_get_full_name():
    """Function to test if full_name property is called"""
    owner = OwnerEntity.create(
        "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
    )
    assert owner.full_name == "Sebastião Maia"


def test_should_get_email():
    """Function to test if email property is called"""
    owner = OwnerEntity.create(
        "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
    )
    assert owner.email.value == "test@mail.com"
