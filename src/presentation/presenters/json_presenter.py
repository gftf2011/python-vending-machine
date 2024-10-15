import json

from typing import Any

from src.presentation.contracts.presenters.base import BasePresenter

from src.domain.contracts.dtos.base import BaseOutput


class JSONPresenter(BasePresenter):
    def execute(self, output: BaseOutput) -> Any:
        return output.to_dict()
