import pytest

from src.domain.entities.product import ProductEntity
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.contracts.services.machine import (
    ChooseProductInputDTO,
    AddCoinsInputDTO,
    AllowDispenseInputDTO,
    DeliverProductInputDTO,
)

from src.services.machine import MachineService
from src.services.exceptions.unregistered_machine import UnregisteredMachineException
from src.services.exceptions.machine_is_not_ready import MachineIsNotReadyException
from src.services.exceptions.product_does_not_exist import ProductDoesNotExistException
from src.services.exceptions.unavailable_product import UnavailableProductException
from src.services.exceptions.incorrect_negative_change import (
    IncorrectNegativeChangeException,
)
from src.services.exceptions.machine_is_not_dispensing import (
    MachineIsNotDispensingException,
)

from src.infra.repositories.machine.stub_machine_repository import (
    FindByIdResponseWithSuccessObject,
    StubMachineRepository,
    UpdateResponseWithSuccessObject,
)


class Test_Machine_Service_Choose_Product:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_registered(self):
        id_value: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(UnregisteredMachineException):
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(None)], []
            )
            service = MachineService(machine_repo)
            input_dto = ChooseProductInputDTO("00", id_value)
            await service.choose_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_ready(self):
        id_value: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(MachineIsNotReadyException):
            products = []
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                id_value, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = ChooseProductInputDTO("00", id_value)
            await service.choose_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_is_not_found(self):
        product_code: str = "00"
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(ProductDoesNotExistException):
            products = []
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = ChooseProductInputDTO(product_code, machine_id)
            await service.choose_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_is_out_of_stock(self):
        product_code: str = "00"
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(UnavailableProductException):
            products = [
                ProductEntity.create(
                    "a9651193-6c44-4568-bdb6-883d703cbee5", "Hersheys", 0, "00", 0
                )
            ]
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = ChooseProductInputDTO(product_code, machine_id)
            await service.choose_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_get_output(self):
        product_code: str = "00"
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"

        products = [
            ProductEntity.create(
                "a9651193-6c44-4568-bdb6-883d703cbee5", "Hersheys", 1, "00", 0
            )
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
        )

        machine_repo = StubMachineRepository(
            [FindByIdResponseWithSuccessObject(machine)], []
        )

        service = MachineService(machine_repo)
        input_dto = ChooseProductInputDTO(product_code, machine_id)

        output = await service.choose_product(input_dto)

        assert output.product_id == "a9651193-6c44-4568-bdb6-883d703cbee5"
        assert output.product_name == "Hersheys"
        assert output.product_price == 0


class Test_Machine_Service_Add_Coins:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_registered(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(UnregisteredMachineException):
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(None)], []
            )
            service = MachineService(machine_repo)
            input_dto = AddCoinsInputDTO(machine_id, 0, 0, 0, 0, 0, 0, 0)
            await service.add_coins(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_ready(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(MachineIsNotReadyException):
            products = []
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = AddCoinsInputDTO(machine_id, 0, 0, 0, 0, 0, 0, 0)
            await service.add_coins(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_change_is_negative(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(IncorrectNegativeChangeException):
            products = []
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
            )
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = AddCoinsInputDTO(machine_id, -1, 0, 0, 0, 0, 0, 0)
            await service.add_coins(input_dto)

    @pytest.mark.asyncio
    async def test_should_return_no_change_when_change_is_0(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"

        products = []
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 1, products
        )

        machine_repo = StubMachineRepository(
            [FindByIdResponseWithSuccessObject(machine)],
            [UpdateResponseWithSuccessObject()],
        )
        service = MachineService(machine_repo)

        input_dto = AddCoinsInputDTO(machine_id, 0, 1, 0, 0, 0, 0, 0)
        output = await service.add_coins(input_dto)

        assert output.coin_01_qty == 0
        assert output.coin_05_qty == 0
        assert output.coin_10_qty == 0
        assert output.coin_25_qty == 0
        assert output.coin_50_qty == 0
        assert output.coin_100_qty == 0

        assert machine.coin_01.qty == 1
        assert machine.coin_05.qty == 0
        assert machine.coin_10.qty == 0
        assert machine.coin_25.qty == 0
        assert machine.coin_50.qty == 0
        assert machine.coin_100.qty == 1

    @pytest.mark.asyncio
    async def test_should_return_change(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"

        products = []
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
        )

        machine_repo = StubMachineRepository(
            [FindByIdResponseWithSuccessObject(machine)],
            [UpdateResponseWithSuccessObject()],
        )
        service = MachineService(machine_repo)

        input_dto = AddCoinsInputDTO(machine_id, 100, 1, 0, 0, 2, 1, 0)
        output = await service.add_coins(input_dto)

        assert output.coin_01_qty == 0
        assert output.coin_05_qty == 0
        assert output.coin_10_qty == 0
        assert output.coin_25_qty == 2
        assert output.coin_50_qty == 1
        assert output.coin_100_qty == 0

        assert machine.coin_01.qty == 1
        assert machine.coin_05.qty == 0
        assert machine.coin_10.qty == 0
        assert machine.coin_25.qty == 0
        assert machine.coin_50.qty == 0
        assert machine.coin_100.qty == 0


class Test_Machine_Service_Allow_Dispense:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_registered(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        with pytest.raises(UnregisteredMachineException):
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(None)], []
            )
            service = MachineService(machine_repo)
            input_dto = AllowDispenseInputDTO(machine_id)
            await service.allow_dispense(input_dto)

    @pytest.mark.asyncio
    async def test_should_update_machine_to_dispensing_state(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"

        products = []
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
        )

        machine_repo = StubMachineRepository(
            [FindByIdResponseWithSuccessObject(machine)],
            [UpdateResponseWithSuccessObject()],
        )
        service = MachineService(machine_repo)

        input_dto = AllowDispenseInputDTO(machine_id)
        await service.allow_dispense(input_dto)

        assert machine.state == MachineState.DISPENSING


class Test_Machine_Service_Deliver_Product:
    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_registered(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_qty: int = 1
        with pytest.raises(UnregisteredMachineException):
            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(None)], []
            )
            service = MachineService(machine_repo)
            input_dto = DeliverProductInputDTO(machine_id, product_id, product_qty)
            await service.deliver_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_is_not_dispensing(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        with pytest.raises(MachineIsNotDispensingException):
            products = [ProductEntity.create(product_id, "Hersheys", 0, "00", 0)]
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.READY, 0, 0, 0, 0, 0, 0, products
            )

            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = DeliverProductInputDTO(machine_id, product_id, 0)
            await service.deliver_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_does_not_exist_in_machine(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id_1: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_id_2: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4d"
        with pytest.raises(ProductDoesNotExistException):
            products = [ProductEntity.create(product_id_1, "Hersheys", 0, "00", 0)]
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products
            )

            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = DeliverProductInputDTO(machine_id, product_id_2, 0)
            await service.deliver_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_there_is_no_available_product_inside_the_machine(
        self,
    ):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        with pytest.raises(UnavailableProductException):
            products = [ProductEntity.create(product_id, "Hersheys", 0, "00", 0)]
            owner = OwnerEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbff5",
                "Sebastião Maia",
                "test@mail.com",
            )
            machine = MachineEntity.create(
                machine_id, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products
            )

            machine_repo = StubMachineRepository(
                [FindByIdResponseWithSuccessObject(machine)], []
            )
            service = MachineService(machine_repo)
            input_dto = DeliverProductInputDTO(machine_id, product_id, 1)
            await service.deliver_product(input_dto)

    @pytest.mark.asyncio
    async def test_should_return_output(
        self,
    ):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        product_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        product_code: str = "00"
        products = [ProductEntity.create(product_id, "Hersheys", 1, product_code, 0)]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5",
            "Sebastião Maia",
            "test@mail.com",
        )
        machine = MachineEntity.create(
            machine_id, owner, MachineState.DISPENSING, 0, 0, 0, 0, 0, 0, products
        )

        machine_repo = StubMachineRepository(
            [FindByIdResponseWithSuccessObject(machine)],
            [UpdateResponseWithSuccessObject()],
        )
        service = MachineService(machine_repo)
        input_dto = DeliverProductInputDTO(machine_id, product_id, 1)
        output = await service.deliver_product(input_dto)

        assert output.product_id == product_id
        assert output.product_code == product_code

        assert machine.products[0].qty == 0
