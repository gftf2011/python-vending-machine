import pytest

from src.domain.value_objects.coins import CoinsValueObject, CoinTypes
from src.domain.exceptions.invalid_coins_qty import InvalidCoinsQtyException


def test_should_raise_exception_by_using_constructor():
    """Function to test if the software component will raise an exception if calls the constructor"""
    with pytest.raises(
        Exception, match="Use the 'create' method to create an instance of this class."
    ):
        CoinsValueObject(CoinTypes.COIN_01, 0)


def test_should_raise_exception_if_coin_quantity_is_negative():
    """Function to test if Coins will raise exception if there quantity is negative"""
    qty = -1
    with pytest.raises(
        InvalidCoinsQtyException, match="quantity of coins can not be negative"
    ):
        CoinsValueObject.create(CoinTypes.COIN_01, qty)


def test_should_get_value():
    """Function to test if value property is called"""
    sut = CoinsValueObject.create(CoinTypes.COIN_05, 0)
    assert sut.value == CoinTypes.COIN_05


def test_should_get_qty():
    """Function to test if qty property is called"""
    sut = CoinsValueObject.create(CoinTypes.COIN_01, 0)
    assert sut.qty == 0


def test_should_increase_qty():
    """Function to test if increase_qty increases quantity of coins"""
    sut = CoinsValueObject.create(CoinTypes.COIN_01, 0)
    sut.increase_qty()
    assert sut.qty == 1


def test_should_reduce_qty():
    """Function to if test reduce_qty reduces quantity of coins"""
    sut = CoinsValueObject.create(CoinTypes.COIN_01, 1)
    sut.reduce_qty()
    assert sut.qty == 0


def test_raise_exception_when_coin_quantity_is_0():
    """Function to test if Coins will raise exception if quantity is reduced below 0"""
    with pytest.raises(
        InvalidCoinsQtyException, match="quantity of coins can not be negative"
    ):
        sut = CoinsValueObject.create(CoinTypes.COIN_01, 0)
        sut.reduce_qty()
