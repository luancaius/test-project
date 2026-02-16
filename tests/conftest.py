"""Shared pytest fixtures for unit tests."""

import pytest

from src.business.models.user import CreateUserRequest, User
from src.infra.cache.in_memory_cache import InMemoryCache
from src.infra.database.in_memory_user_database import InMemoryUserDatabase
from src.infra.repositories.user_repository import UserRepository
from src.business.services.user_service import UserService


@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="Alice", email="alice@example.com", age=30)


@pytest.fixture
def sample_user_2() -> User:
    return User(id=2, name="Bob", email="bob@example.com", age=25)


@pytest.fixture
def create_user_request() -> CreateUserRequest:
    return CreateUserRequest(name="Charlie", email="charlie@example.com", age=35)


@pytest.fixture
def in_memory_database() -> InMemoryUserDatabase:
    return InMemoryUserDatabase()


@pytest.fixture
def cache_with_ttl_60() -> InMemoryCache:
    """Cache with 60s TTL for normal (non-expiry) tests."""
    return InMemoryCache(ttl_seconds=60)


@pytest.fixture
def cache_ttl_1_second() -> InMemoryCache:
    """Cache with 1s TTL for expired-cache tests."""
    return InMemoryCache(ttl_seconds=1)


@pytest.fixture
def user_repository(in_memory_database, cache_with_ttl_60) -> UserRepository:
    return UserRepository(cache=cache_with_ttl_60, database=in_memory_database)


@pytest.fixture
def user_service(user_repository) -> UserService:
    return UserService(repository=user_repository)
