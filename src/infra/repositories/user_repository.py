from typing import cast

from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.infra.cache.cache import Cache
from src.infra.database.database import Database
from src.shared.logger import logger

KEY_USERS = "users"


class UserRepository:
    def __init__(self, cache: Cache, database: Database) -> None:
        self._cache = cache
        self._database = database

    def get_all(self) -> list[User]:
        # cached = self._cache.get(KEY_USERS)
        # if cached is not None:
        #     logger.info("users_listed_from_cache", count=len(cached))
        #     return cast(list[User], cached)
        # logger.info("users_listed_from_database")
        users = self._database.get(KEY_USERS)
        # self._cache.set(KEY_USERS, users)
        return users

    def get_by_id(self, user_id: int) -> User | None:
        cached = self._cache.get(f"{KEY_USERS}:{user_id}")
        if cached is not None:
            logger.info("user_found_in_cache", user_id=user_id)
            return cast(User, cached)
        logger.info("user_not_found_in_cache", user_id=user_id)
        user = self._database.get(KEY_USERS, user_id)
        if user is not None:
            self._cache.set(f"{KEY_USERS}:{user_id}", user)
            return user
        logger.info("user_not_found_in_database", user_id=user_id)
        return None

    def create(self, data: CreateUserRequest) -> User:
        user = self._database.create(KEY_USERS, data)
        self._cache.set(f"{KEY_USERS}:{user.id}", user)
        logger.info("user_created", user_id=user.id)
        return user

    def update(self, user_id: int, data: UpdateUserRequest) -> User | None:
        user = self._database.update(KEY_USERS, user_id, data)
        if user is not None:
            self._cache.set(f"{KEY_USERS}:{user_id}", user)
            logger.info("user_updated", user_id=user_id)
            return user
        logger.info("user_not_found_in_database", user_id=user_id)
        return None
