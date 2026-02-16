
from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.infra.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def get_all(self) -> list[User]:
        users = self._repository.get_all()
        return users

    def get_by_id(self, user_id: int) -> User | None:
        user = self._repository.get_by_id(user_id)
        return user

    def create_user(
        self,
        name: str,
        email: str,
        age: int | None = None,
    ) -> User:
        data = CreateUserRequest(name=name, email=email, age=age)
        created = self._repository.create(data)
        return created

    def update_user(
        self,
        user_id: int,
        name: str | None = None,
        email: str | None = None,
        age: int | None = None,
    ) -> User | None:
        data = UpdateUserRequest(name=name, email=email, age=age)
        updated = self._repository.update(user_id=user_id, data=data)
        return updated
