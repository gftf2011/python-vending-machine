from datetime import datetime

import pytest

from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity
from src.domain.entities.payment import PaymentType

from src.services.contracts.controllers.machine import (
    ChooseProductInputControllerDTO,
    PayForProductInputControllerDTO,
)

from src.presentation.controllers.machine import (
    MachineController,
)

from src.presentation.presenters.json_presenter import JSONPresenter

from src.services.machine import MachineService
from src.services.order import OrderService
from src.services.payment import PaymentService

from src.infra.repositories.machine.fake_machine_repository import FakeMachineRepository
from src.infra.repositories.order.fake_order_repository import FakeOrderRepository
from src.infra.repositories.payment.fake_payment_repository import FakePaymentRepository


class Test_Machine_Controller_Choose_Product:
    @pytest.fixture(autouse=True)
    def reset_fake_repos(self):
        FakeMachineRepository.reset_instance()
        FakeOrderRepository.reset_instance()
        FakePaymentRepository.reset_instance()

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_registered(self):
        machine_repo = FakeMachineRepository.get_instance()
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter,
            machine_service,
            order_service,
            payment_service,
        )

        output = await machine_controller.choose_product(
            ChooseProductInputControllerDTO("00", "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f")
        )

        assert (
            output[0]["error"]["message"]
            == 'machine - "' + "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f" + '" - is not registered in the system'
        )
        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_ready(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter,
            machine_service,
            order_service,
            payment_service,
        )

        output = await machine_controller.choose_product(ChooseProductInputControllerDTO(products[0].code, machine_id))

        assert output[0]["error"]["message"] == "machine is not READY for operation"

        assert output[1] == 400

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_product_does_not_exists(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.choose_product(ChooseProductInputControllerDTO("03", machine_id))

        assert output[0]["error"]["message"] == "product does not exists"

        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_product_is_out_of_stock(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 0, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.choose_product(ChooseProductInputControllerDTO(products[0].code, machine_id))

        assert (
            output[0]["error"]["message"]
            == 'product - "' + products[0].id.value + '" - is not available in the machine'
        )

        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_return_output(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.choose_product(ChooseProductInputControllerDTO(products[0].code, machine_id))

        loaded_output = output[0]

        assert loaded_output["product_id"] == products[0].id.value
        assert loaded_output["product_price"] == products[0].unit_price
        assert loaded_output["product_name"] == products[0].name

        assert output[1] == 200


class Test_Machine_Controller_Pay_For_Product:
    @pytest.fixture(autouse=True)
    def reset_fake_repos(self):
        FakeMachineRepository.reset_instance()
        FakeOrderRepository.reset_instance()
        FakePaymentRepository.reset_instance()

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_registered(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter,
            machine_service,
            order_service,
            payment_service,
        )

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f",
                products[0].id.value,
                0,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                0,
                0,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert (
            output[0]["error"]["message"]
            == 'machine - "' + "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4f" + '" - is not registered in the system'
        )
        assert output[0]["error"]["data"]["coin_01"] == 0
        assert output[0]["error"]["data"]["coin_05"] == 0
        assert output[0]["error"]["data"]["coin_10"] == 0
        assert output[0]["error"]["data"]["coin_25"] == 0
        assert output[0]["error"]["data"]["coin_50"] == 0
        assert output[0]["error"]["data"]["coin_100"] == 0

        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_return_error_message_if_machine_is_not_ready(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(
            json_presenter,
            machine_service,
            order_service,
            payment_service,
        )

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                machine_id,
                products[0].id.value,
                0,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                0,
                0,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert output[0]["error"]["message"] == "machine is not READY for operation"
        assert output[0]["error"]["data"]["coin_01"] == 0
        assert output[0]["error"]["data"]["coin_05"] == 0
        assert output[0]["error"]["data"]["coin_10"] == 0
        assert output[0]["error"]["data"]["coin_25"] == 0
        assert output[0]["error"]["data"]["coin_50"] == 0
        assert output[0]["error"]["data"]["coin_100"] == 0

        assert output[1] == 400

    @pytest.mark.asyncio
    async def test_should_return_error_if_change_is_negative(self):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                machine_id,
                products[0].id.value,
                1,
                PaymentType.CASH,
                4,
                0,
                2,
                1,
                1,
                0,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert output[0]["error"]["message"] == "change can not be negative"
        assert output[0]["error"]["data"]["coin_01"] == 4
        assert output[0]["error"]["data"]["coin_05"] == 0
        assert output[0]["error"]["data"]["coin_10"] == 2
        assert output[0]["error"]["data"]["coin_25"] == 1
        assert output[0]["error"]["data"]["coin_50"] == 1
        assert output[0]["error"]["data"]["coin_100"] == 0

        assert output[1] == 416

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_does_not_exists(
        self,
    ):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                machine_id,
                "b9651752-6c44-4578-bdb6-883d703cbffe",
                1,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                0,
                0,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert output[0]["error"]["message"] == "product does not exists"
        assert output[0]["error"]["data"]["coin_01"] == 0
        assert output[0]["error"]["data"]["coin_05"] == 0
        assert output[0]["error"]["data"]["coin_10"] == 0
        assert output[0]["error"]["data"]["coin_25"] == 0
        assert output[0]["error"]["data"]["coin_50"] == 0
        assert output[0]["error"]["data"]["coin_100"] == 0

        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_product_is_out_of_stock(
        self,
    ):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 0, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                machine_id,
                products[0].id.value,
                1,
                PaymentType.CASH,
                0,
                1,
                0,
                0,
                0,
                0,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert (
            output[0]["error"]["message"]
            == 'product - "' + products[0].id.value + '" - is not available in the machine'
        )
        assert output[0]["error"]["data"]["coin_01"] == 0
        assert output[0]["error"]["data"]["coin_05"] == 1
        assert output[0]["error"]["data"]["coin_10"] == 0
        assert output[0]["error"]["data"]["coin_25"] == 0
        assert output[0]["error"]["data"]["coin_50"] == 0
        assert output[0]["error"]["data"]["coin_100"] == 0

        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_machine_does_not_have_enough_coins_to_return(
        self,
    ):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                machine_id,
                products[1].id.value,
                1,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                1,
                1,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert output[0]["error"]["message"] == "not enough change in the machine"
        assert output[0]["error"]["data"]["coin_01"] == 0
        assert output[0]["error"]["data"]["coin_05"] == 0
        assert output[0]["error"]["data"]["coin_10"] == 0
        assert output[0]["error"]["data"]["coin_25"] == 0
        assert output[0]["error"]["data"]["coin_50"] == 1
        assert output[0]["error"]["data"]["coin_100"] == 1

        assert output[1] == 404

    @pytest.mark.asyncio
    async def test_should_return_change(
        self,
    ):
        machine_id: str = "43c6fc3c-a51a-4c5d-9c1d-aae7e0c6ac4e"
        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbfff", "Hersheys", 1, "00", 100),
            ProductEntity.create(
                "b9651752-6c44-4578-bdb6-883d703cc000",
                "Almond Joy Candy Bar",
                1,
                "01",
                125,
            ),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cc001", "Twix Candy Bars", 1, "02", 75),
        ]
        owner = OwnerEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Sebastião Maia", "test@mail.com")
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
        order_repo = FakeOrderRepository.get_instance()
        payment_repo = FakePaymentRepository.get_instance()

        await machine_repo.save(machine)

        machine_service = MachineService(machine_repo)
        order_service = OrderService(machine_repo, order_repo)
        payment_service = PaymentService(order_repo, payment_repo)

        json_presenter = JSONPresenter()
        machine_controller = MachineController(json_presenter, machine_service, order_service, payment_service)

        output = await machine_controller.pay_for_product(
            PayForProductInputControllerDTO(
                machine_id,
                products[0].id.value,
                1,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                0,
                2,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

        assert output[0]["coin_01_qty"] == 0
        assert output[0]["coin_05_qty"] == 0
        assert output[0]["coin_10_qty"] == 0
        assert output[0]["coin_25_qty"] == 0
        assert output[0]["coin_50_qty"] == 0
        assert output[0]["coin_100_qty"] == 1

        assert output[1] == 201
