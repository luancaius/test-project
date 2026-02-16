from abc import ABC, abstractmethod

from src.business.models.user import CreateUserRequest, UpdateUserRequest, User


class Database(ABC):
    """Storage for user data. Used by UserRepository after cache miss."""

    @abstractmethod
    def get(self, key: str, user_id: int | None = None) -> list[User] | User | None:
        """Return all users when user_id is None; return one user by id when user_id is set."""
        pass

    @abstractmethod
    def create(self, key: str, data: CreateUserRequest) -> User:
        pass

    @abstractmethod
    def update(self, key: str, user_id: int, data: UpdateUserRequest) -> User | None:
        pass
