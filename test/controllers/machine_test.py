import json
import pytest

from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity

from src.presentation.controllers.machine import (
    ChooseProductInputControllerDTO,
    AddCoinsInputControllerDTO,
    MachineController,
)

from src.presentation.presenters.json_presenter import JSONPresenter

from src.services.machine import MachineService

from src.infra.repositories.machine.fake_machine_repository import FakeMachineRepository


class Test_Machine_Controller_Choose_Product:
    @pytest.fixture(autouse=True)
    def reset_fake_repos(self):
        FakeMachineRepository.reset_instance()

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_registered(self):
        machine_repo = FakeMachineRepository.get_instance()

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        )

        output = await machine_controller.choose_product(
            ChooseProductInputControllerDTO("00")
        )

        assert (
            json.loads(output)["error"]["message"]
            == 'machine - "'
            + "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
            + '" - is not registered in the system'
        )

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_ready(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75
            ),
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.DISPENSING,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        machine_repo = FakeMachineRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, machine_id
        )

        output = await machine_controller.choose_product(
            ChooseProductInputControllerDTO(products[0].code)
        )

        assert (
            json.loads(output)["error"]["message"]
            == "machine is not READY for operation"
        )

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_product_does_not_exists(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75
            ),
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.READY,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        machine_repo = FakeMachineRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, machine_id
        )

        output = await machine_controller.choose_product(
            ChooseProductInputControllerDTO("03")
        )

        assert json.loads(output)["error"]["message"] == "product does not exists"

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_product_is_out_of_stock(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 0, "00", 100
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75
            ),
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.READY,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        machine_repo = FakeMachineRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, machine_id
        )

        output = await machine_controller.choose_product(
            ChooseProductInputControllerDTO(products[0].code)
        )

        assert (
            json.loads(output)["error"]["message"]
            == 'product - "'
            + products[0].id.value
            + '" - is not available in the machine'
        )

    @pytest.mark.asyncio
    async def test_should_return_output(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75
            ),
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.READY,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        machine_repo = FakeMachineRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, machine_id
        )

        output = await machine_controller.choose_product(
            ChooseProductInputControllerDTO(products[0].code)
        )

        loaded_output = json.loads(output)

        assert loaded_output["product_id"] == products[0].id.value
        assert loaded_output["product_price"] == products[0].unit_price
        assert loaded_output["product_name"] == products[0].name


class Test_Machine_Controller_Add_coins:
    @pytest.fixture(autouse=True)
    def reset_fake_repos(self):
        FakeMachineRepository.reset_instance()

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_registered(self):
        machine_repo = FakeMachineRepository.get_instance()

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
        )

        output = await machine_controller.add_coins(
            AddCoinsInputControllerDTO(0, 0, 0, 0, 0, 0, 0)
        )

        assert (
            json.loads(output)["error"]["message"]
            == 'machine - "'
            + "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f"
            + '" - is not registered in the system'
        )
        assert json.loads(output)["error"]["data"]["coin_01"] == 0
        assert json.loads(output)["error"]["data"]["coin_05"] == 0
        assert json.loads(output)["error"]["data"]["coin_10"] == 0
        assert json.loads(output)["error"]["data"]["coin_25"] == 0
        assert json.loads(output)["error"]["data"]["coin_50"] == 0
        assert json.loads(output)["error"]["data"]["coin_100"] == 0

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_ready(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75
            ),
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.DISPENSING,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        machine_repo = FakeMachineRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, machine_id
        )

        output = await machine_controller.add_coins(
            AddCoinsInputControllerDTO(0, 0, 0, 0, 0, 0, 0)
        )

        assert (
            json.loads(output)["error"]["message"]
            == "machine is not READY for operation"
        )
        assert json.loads(output)["error"]["data"]["coin_01"] == 0
        assert json.loads(output)["error"]["data"]["coin_05"] == 0
        assert json.loads(output)["error"]["data"]["coin_10"] == 0
        assert json.loads(output)["error"]["data"]["coin_25"] == 0
        assert json.loads(output)["error"]["data"]["coin_50"] == 0
        assert json.loads(output)["error"]["data"]["coin_100"] == 0

    @pytest.mark.asyncio
    async def test_should_return_error_if_change_is_negative(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75
            ),
        ]
        owner = OwnerEntity.create(
            "b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com"
        )
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.READY,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        machine_repo = FakeMachineRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter, machine_service, machine_id
        )

        output = await machine_controller.add_coins(
            AddCoinsInputControllerDTO(-1, 1, 1, 1, 1, 1, 1)
        )

        assert json.loads(output)["error"]["message"] == "change can not be negative"
        assert json.loads(output)["error"]["data"]["coin_01"] == 1
        assert json.loads(output)["error"]["data"]["coin_05"] == 1
        assert json.loads(output)["error"]["data"]["coin_10"] == 1
        assert json.loads(output)["error"]["data"]["coin_25"] == 1
        assert json.loads(output)["error"]["data"]["coin_50"] == 1
        assert json.loads(output)["error"]["data"]["coin_100"] == 1
