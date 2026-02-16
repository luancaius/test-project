from abc import ABC, abstractmethod
from typing import Optional

from src.business.models.user import User


class UserCache(ABC):
    """Cache for User entities. GETs hit this before the repository."""

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def set_user(self, user_id: int, user: User) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> Optional[list[User]]:
        """Returns None on cache miss."""
        pass

    @abstractmethod
    def set_all_users(self, users: list[User]) -> None:
        pass

    @abstractmethod
    def invalidate_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def invalidate_all(self) -> None:
        pass
