from datetime import datetime

import pytest

from src.domain.entities.payment import PaymentType
from src.domain.contracts.dtos.machine import ChooseProductOutputDTO, AddCoinsOutputDTO

from src.services.contracts.controllers.machine import ChooseProductInputControllerDTO, PayForProductInputControllerDTO

from src.presentation.controllers.decorators.machine_transaction_decorator import MachineTransactionDecorator
from src.presentation.controllers.stub_machine import (
    StubMachineController,
    ChooseProductResponseWithSuccessObject,
    PayForProductResponseWithSuccessObject,
)

from src.infra.database.postgres.spy_transaction import (
    SpyTransaction,
    CreateClientResponseWithSuccessObject,
    CommitResponseWithSuccessObject,
    OpenTransactionResponseWithSuccessObject,
    ReleaseResponseWithSuccessObject,
    RollbackResponseWithSuccessObject,
)


class Test_Machine_Transaction_Decorator:
    @pytest.mark.asyncio
    async def test_should_commit_choose_product_decoratee_response(self):
        decoratee = StubMachineController(
            [ChooseProductResponseWithSuccessObject([ChooseProductOutputDTO("fake_id", 0, "fake_name"), 200])], []
        )
        spy_transaction = SpyTransaction(
            [],
            [],
            [OpenTransactionResponseWithSuccessObject(None)],
            [ReleaseResponseWithSuccessObject(None)],
            [CreateClientResponseWithSuccessObject(None)],
            [CommitResponseWithSuccessObject(None)],
            [],
            [],
        )
        sut = MachineTransactionDecorator(decoratee, spy_transaction)
        result = await sut.choose_product(ChooseProductInputControllerDTO("01", "eb56f21b-57fe-4534-81ca-afa42f7ca6d5"))

        assert result[1] == 200

        assert spy_transaction.create_client_counter == 1
        assert spy_transaction.open_transaction_counter == 1
        assert spy_transaction.commit_counter == 1
        assert spy_transaction.release_counter == 1

        assert spy_transaction.rollback_counter == 0
        assert spy_transaction.close_counter == 0

    @pytest.mark.asyncio
    async def test_should_commit_pay_for_product_decoratee_response(self):
        decoratee = StubMachineController(
            [], [PayForProductResponseWithSuccessObject([AddCoinsOutputDTO(0, 0, 0, 0, 0, 0, 0), 201])]
        )
        spy_transaction = SpyTransaction(
            [],
            [],
            [OpenTransactionResponseWithSuccessObject(None)],
            [ReleaseResponseWithSuccessObject(None)],
            [CreateClientResponseWithSuccessObject(None)],
            [CommitResponseWithSuccessObject(None)],
            [],
            [],
        )
        sut = MachineTransactionDecorator(decoratee, spy_transaction)
        result = await sut.pay_for_product(
            PayForProductInputControllerDTO(
                "fake_machine_id",
                "fake_product_id",
                0,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                0,
                0,
                datetime(1970, 1, 1).isoformat(timespec="seconds"),
            )
        )

        assert result[1] == 201

        assert spy_transaction.create_client_counter == 1
        assert spy_transaction.open_transaction_counter == 1
        assert spy_transaction.commit_counter == 1
        assert spy_transaction.release_counter == 1

        assert spy_transaction.rollback_counter == 0
        assert spy_transaction.close_counter == 0

    @pytest.mark.asyncio
    async def test_should_rollback_choose_product_decoratee_response(self):
        decoratee = StubMachineController(
            [ChooseProductResponseWithSuccessObject([ChooseProductOutputDTO("fake_id", 0, "fake_name"), 400])], []
        )
        spy_transaction = SpyTransaction(
            [],
            [],
            [OpenTransactionResponseWithSuccessObject(None)],
            [ReleaseResponseWithSuccessObject(None)],
            [CreateClientResponseWithSuccessObject(None)],
            [],
            [RollbackResponseWithSuccessObject(None)],
            [],
        )
        sut = MachineTransactionDecorator(decoratee, spy_transaction)
        result = await sut.choose_product(ChooseProductInputControllerDTO("01", "eb56f21b-57fe-4534-81ca-afa42f7ca6d5"))

        assert result[1] == 400

        assert spy_transaction.create_client_counter == 1
        assert spy_transaction.open_transaction_counter == 1
        assert spy_transaction.commit_counter == 0
        assert spy_transaction.release_counter == 1

        assert spy_transaction.rollback_counter == 1
        assert spy_transaction.close_counter == 0

    @pytest.mark.asyncio
    async def test_should_rollback_pay_for_product_decoratee_response(self):
        decoratee = StubMachineController(
            [], [PayForProductResponseWithSuccessObject([AddCoinsOutputDTO(0, 0, 0, 0, 0, 0, 0), 400])]
        )
        spy_transaction = SpyTransaction(
            [],
            [],
            [OpenTransactionResponseWithSuccessObject(None)],
            [ReleaseResponseWithSuccessObject(None)],
            [CreateClientResponseWithSuccessObject(None)],
            [],
            [RollbackResponseWithSuccessObject(None)],
            [],
        )
        sut = MachineTransactionDecorator(decoratee, spy_transaction)
        result = await sut.pay_for_product(
            PayForProductInputControllerDTO(
                "fake_machine_id",
                "fake_product_id",
                0,
                PaymentType.CASH,
                0,
                0,
                0,
                0,
                0,
                0,
                datetime(1970, 1, 1).isoformat(timespec="seconds"),
            )
        )

        assert result[1] == 400

        assert spy_transaction.create_client_counter == 1
        assert spy_transaction.open_transaction_counter == 1
        assert spy_transaction.commit_counter == 0
        assert spy_transaction.release_counter == 1

        assert spy_transaction.rollback_counter == 1
        assert spy_transaction.close_counter == 0
