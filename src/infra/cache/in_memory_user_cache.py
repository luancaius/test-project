import time

from src.business.models.user import User
from src.infra.cache.user_cache import UserCache


class InMemoryUserCache(UserCache):
    """In-memory user cache with TTL. Entries expire after ttl_seconds."""

    _ALL_KEY = "__all__"

    def __init__(self, ttl_seconds: int = 60) -> None:
        self._ttl_seconds = ttl_seconds
        self._by_id: dict[int, tuple[User, float]] = {}
        self._all: tuple[list[User], float] | None = None

    def _now(self) -> float:
        return time.time()

    def _expired(self, at: float) -> bool:
        return self._now() > at + self._ttl_seconds

    def get_user(self, user_id: int) -> User | None:
        entry = self._by_id.get(user_id)
        if entry is None:
            return None
        user, at = entry
        if self._expired(at):
            del self._by_id[user_id]
            return None
        return user

    def set_user(self, user_id: int, user: User) -> None:
        self._by_id[user_id] = (user, self._now())

    def get_all_users(self) -> list[User] | None:
        if self._all is None:
            return None
        users, at = self._all
        if self._expired(at):
            self._all = None
            return None
        return list(users)

    def set_all_users(self, users: list[User]) -> None:
        self._all = (list(users), self._now())

    def invalidate_user(self, user_id: int) -> None:
        self._by_id.pop(user_id, None)

    def invalidate_all(self) -> None:
        self._by_id.clear()
        self._all = None
