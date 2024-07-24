import pytest

from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity
from src.domain.entities.machine import MachineEntity, MachineState

from src.domain.exceptions.invalid_coins_qty import InvalidCoinsQtyException
from src.domain.exceptions.no_change_available import NoChangeAvailableException

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        MachineEntity("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])

def test_should_get_id():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_id().get_value() == "a8351752-ec32-4578-bdb6-883d703cbee7"

def test_should_get_state():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_state() == MachineState.READY

def test_should_start_dispense_product():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    machine.start_dispense_product()
    assert machine.get_state() == MachineState.DISPENSING

def test_should_finish_dispense_product():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, [])
    machine.finish_dispense_product()
    assert machine.get_state() == MachineState.READY

def test_should_get_coin_01():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_coin_01().get_qty() == 0

def test_should_get_coin_05():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_coin_05().get_qty() == 0

def test_should_get_coin_10():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_coin_10().get_qty() == 0

def test_should_get_coin_25():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_coin_25().get_qty() == 0

def test_should_get_coin_50():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_coin_50().get_qty() == 0

def test_should_get_coin_100():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, [])
    assert machine.get_coin_100().get_qty() == 0

def test_should_get_products():
    products = [ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 0, "00", 0)]
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
    assert machine.get_products()[0].get_id().get_value() == "b9651752-6c44-4578-bdb6-883d703cbfff"
    assert machine.get_products()[0].get_name() == "Hersheys"
    assert machine.get_products()[0].get_code() == "00"
    assert machine.get_products()[0].get_qty() == 0
    assert machine.get_products()[0].get_unit_price() == 0

def test_should_get_owner():
    products = []
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
    assert machine.get_owner().get_id().get_value() == "b9651752-6c44-4578-bdb6-883d703cbff5"
    assert machine.get_owner().get_full_name() == "Sebastião Maia"
    assert machine.get_owner().get_email().get_value() == "test@mail.com"

def test_should_add_coins():
    products = []
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
    
    machine.add_coins(1, 1, 1, 1, 1, 1)
    
    assert machine.get_coin_01().get_qty() == 1
    assert machine.get_coin_05().get_qty() == 1
    assert machine.get_coin_10().get_qty() == 1
    assert machine.get_coin_25().get_qty() == 1
    assert machine.get_coin_50().get_qty() == 1
    assert machine.get_coin_100().get_qty() == 1

def test_should_subtract_coins():
    products = []
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 1, 1, 1, 1, 1, 1, products)
    
    machine.subtract_coins(1, 1, 1, 1, 1, 1)
    
    assert machine.get_coin_01().get_qty() == 0
    assert machine.get_coin_05().get_qty() == 0
    assert machine.get_coin_10().get_qty() == 0
    assert machine.get_coin_25().get_qty() == 0
    assert machine.get_coin_50().get_qty() == 0
    assert machine.get_coin_100().get_qty() == 0

def test_should_raise_exception_when_there_is_enough_coins_to_subtract():
    with pytest.raises(InvalidCoinsQtyException, match="quantity of coins can not be negative"):
        products = []
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 1, 1, 1, 1, 1, 1, products)
        machine.subtract_coins(1, 1, 1, 1, 1, 2)

def test_should_get_amount_out_of_coins():
    products = []
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
    amount: int = machine.get_amount_out_of_coins(1, 1, 1, 1, 1, 1)
    assert amount == 191

def test_should_get_amount_out_of_coins():
    products = []
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
    amount: int = machine.get_amount_out_of_coins(1, 1, 1, 1, 1, 1)
    assert amount == 191

def test_should_raise_exception_if_machine_does_not_have_enough_coins_for_change():
    with pytest.raises(NoChangeAvailableException, match="not enough change in the machine"):
        products = []
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products)
        change: int = 1
        machine.get_coins_from_change(change)

def test_should_get_coins_from_change():
    products = []
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineEntity.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 1, 0, 0, 0, 0, 0, products)
    change: int = 1
    coins_change = machine.get_coins_from_change(change)
    assert coins_change.coin_01_qty == 1
    assert coins_change.coin_05_qty == 0
    assert coins_change.coin_10_qty == 0
    assert coins_change.coin_25_qty == 0
    assert coins_change.coin_50_qty == 0
    assert coins_change.coin_100_qty == 0
