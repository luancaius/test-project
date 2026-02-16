from abc import ABC, abstractmethod
from typing import Any, Optional


class Cache(ABC):
    """Generic key-value cache. GETs hit this before the database."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass
