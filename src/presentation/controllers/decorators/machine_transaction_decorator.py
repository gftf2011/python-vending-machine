from typing import Any

from src.services.contracts.database.base import IDatabaseTransaction

from src.services.contracts.controllers.machine import (
    IMachineController,
    ChooseProductInputControllerDTO,
    PayForProductInputControllerDTO,
)


class MachineTransactionDecorator(IMachineController):
    def __init__(
        self,
        decoratee: IMachineController,
        transaction: IDatabaseTransaction,
    ):
        self._decoratee = decoratee
        self._transaction = transaction

    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        await self._transaction.create_client()
        await self._transaction.open_transaction()
        response = await self._decoratee.choose_product(input_dto)
        if response[1] == 200:
            await self._transaction.commit()
            await self._transaction.release()
        else:
            await self._transaction.rollback()
            await self._transaction.release()
        return response

    async def pay_for_product(self, input_dto: PayForProductInputControllerDTO) -> Any:
        await self._transaction.create_client()
        await self._transaction.open_transaction()
        response = await self._decoratee.pay_for_product(input_dto)
        if response[1] == 201:
            await self._transaction.commit()
            await self._transaction.release()
        else:
            await self._transaction.rollback()
            await self._transaction.release()
        return response
