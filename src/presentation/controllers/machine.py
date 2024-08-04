from typing import Any

from src.domain.contracts.dtos.base import BaseOutput

from src.domain.contracts.dtos.machine import (
    ChooseProductOutputDTO,
    ChooseProductInputDTO,
)

from src.domain.contracts.services.machine import IMachineService

from src.presentation.contracts.presenters.base import BasePresenter


class ChooseProductInputControllerDTO:
    def __init__(self, product_code: str):
        self.product_code = product_code


class ChooseProductErrorOutputControllerDTO(BaseOutput):
    def __init__(self, error: str):
        self.error = error

    def to_dict(self) -> Any:
        return {"error": self.error}


class MachineController:
    def __init__(
        self,
        presenter: BasePresenter,
        machine_service: IMachineService,
        machine_id: str,
    ):
        self._presenter = presenter
        self._machine_service = machine_service
        self._machine_id = machine_id

    async def choose_product(self, input_dto: ChooseProductInputControllerDTO) -> Any:
        try:
            output: ChooseProductOutputDTO = await self._machine_service.choose_product(
                ChooseProductInputDTO(input_dto.product_code, self._machine_id)
            )
            return self._presenter.execute(output)
        except Exception as error:
            return self._presenter.execute(
                ChooseProductErrorOutputControllerDTO(str(error))
            )
