import pytest

from src.domain.value_objects.coins import CoinsValueObject, CoinTypes
from src.domain.exceptions.invalid_coins_qty import InvalidCoinsQty

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        CoinsValueObject(CoinTypes.COIN_01, 0)

def test_should_raise_exception_if_coin_quantity_is_negative():
    qty = -1
    with pytest.raises(InvalidCoinsQty, match="quantity of coins can not be negative"):
        CoinsValueObject.create(CoinTypes.COIN_01, qty)

def test_should_get_value():
    sut = CoinsValueObject.create(CoinTypes.COIN_05, 0)
    assert sut.get_value() == CoinTypes.COIN_05

def test_should_get_qty():
    sut = CoinsValueObject.create(CoinTypes.COIN_01, 0)
    assert sut.get_qty() == 0

def test_should_increase_qty():
    sut = CoinsValueObject.create(CoinTypes.COIN_01, 0)
    sut.increase_qty()
    assert sut.get_qty() == 1

def test_should_reduce_qty():
    sut = CoinsValueObject.create(CoinTypes.COIN_01, 1)
    sut.reduce_qty()
    assert sut.get_qty() == 0

def test_raise_exception_when_coin_quantity_is_0():
    with pytest.raises(InvalidCoinsQty, match="quantity of coins can not be negative"):
        sut = CoinsValueObject.create(CoinTypes.COIN_01, 0)
        sut.reduce_qty()