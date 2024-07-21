import pytest

from src.domain.entities.owner import OwnerEntity
from src.domain.entities.machine import MachineAggregate, MachineState

def test_should_raise_exception_by_using_constructor():
    with pytest.raises(Exception, match="Use the 'create' method to create an instance of this class."):
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
        MachineAggregate("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0)

def test_should_get_id():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineAggregate.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0)
    assert machine.get_id() == "a8351752-ec32-4578-bdb6-883d703cbee7"

def test_should_get_state():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineAggregate.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0)
    assert machine.get_state() == MachineState.READY

def test_should_start_dispense_product():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineAggregate.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0)
    machine.start_dispense_product()
    assert machine.get_state() == MachineState.DISPENSING

def test_should_finish_dispense_product():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineAggregate.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0)
    machine.finish_dispense_product()
    assert machine.get_state() == MachineState.READY

def test_should_get_coin_01_qty():
    owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
    machine = MachineAggregate.create("a8351752-ec32-4578-bdb6-883d703cbee7", owner, MachineState.READY, 0, 0, 0, 0, 0, 0)
    assert machine.get_coin_01_qty() == 0