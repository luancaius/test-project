
from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.infra.database.database import Database


class InMemoryUserDatabase(Database):
    """In-memory user store. No TTL; data persists until app restart."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id = 1

    def get(self, key: str, user_id: int | None = None) -> list[User] | User | None:
        if user_id is not None:
            return self._users.get(user_id)
        return list(self._users.values())

    def create(self, key: str, data: CreateUserRequest) -> User:
        user = User(
            id=self._next_id,
            name=data.name,
            email=data.email,
            age=data.age,
        )
        self._next_id += 1
        self._users[user.id] = user
        return user

    def update(self, key: str, user_id: int, data: UpdateUserRequest) -> User | None:
        user = self._users.get(user_id)
        if user is None:
            return None
        updated = User(
            id=user.id,
            name=data.name if data.name is not None else user.name,
            email=data.email if data.email is not None else user.email,
            age=data.age if data.age is not None else user.age,
        )
        self._users[user_id] = updated
        return updated
