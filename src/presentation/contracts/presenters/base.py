from typing import Any

from abc import ABC, abstractmethod

from src.domain.contracts.dtos.base import BaseOutput


class BasePresenter(ABC):
    @abstractmethod
    def execute(self, output: BaseOutput) -> Any:
        pass
