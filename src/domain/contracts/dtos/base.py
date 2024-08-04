from abc import ABC, abstractmethod

from typing import Any


class BaseOutput(ABC):
    @abstractmethod
    def to_dict(self) -> Any:
        pass
