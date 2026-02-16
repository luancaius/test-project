from typing import Optional

from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.infra.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def get_all(self) -> list[User]:
        users = self._repository.get_all()
        return users

    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self._repository.get_by_id(user_id)
        return user

    def create_user(
        self,
        name: str,
        email: str,
        age: Optional[int] = None,
    ) -> User:
        data = CreateUserRequest(name=name, email=email, age=age)
        created = self._repository.create(data)
        return created

    def update_user(
        self,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        age: Optional[int] = None,
    ) -> Optional[User]:
        data = UpdateUserRequest(name=name, email=email, age=age)
        updated = self._repository.update(user_id=user_id, data=data)
        return updated
