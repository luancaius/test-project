import time
from unittest.mock import MagicMock

import pytest

from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.infra.cache.in_memory_cache import InMemoryCache
from src.infra.repositories.user_repository import UserRepository


@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="Alice", email="alice@example.com", age=30)


@pytest.fixture
def mock_database(sample_user: User) -> MagicMock:
    db = MagicMock()
    db.get.return_value = None
    db.create.return_value = sample_user
    db.update.return_value = sample_user
    return db


def test_get_by_id_cache_hit_does_not_call_database(
    sample_user: User,
    mock_database: MagicMock,
) -> None:
    cache = InMemoryCache(ttl_seconds=60)
    cache.set("users:1", sample_user)
    repo = UserRepository(cache=cache, database=mock_database)

    result = repo.get_by_id(1)

    assert result == sample_user
    mock_database.get.assert_not_called()


def test_get_by_id_cache_miss_calls_database_and_populates_cache(
    sample_user: User,
    mock_database: MagicMock,
) -> None:
    mock_database.get.return_value = sample_user
    cache = InMemoryCache(ttl_seconds=60)
    repo = UserRepository(cache=cache, database=mock_database)

    result = repo.get_by_id(1)

    assert result == sample_user
    mock_database.get.assert_called_once_with("users", 1)
    assert cache.get("users:1") == sample_user


def test_get_by_id_cache_miss_user_not_in_database_returns_none(
    mock_database: MagicMock,
) -> None:
    mock_database.get.return_value = None
    cache = InMemoryCache(ttl_seconds=60)
    repo = UserRepository(cache=cache, database=mock_database)

    result = repo.get_by_id(999)

    assert result is None
    mock_database.get.assert_called_once_with("users", 999)
    assert cache.get("users:999") is None


def test_get_by_id_expired_cache_hits_database_and_repopulates_cache(
    sample_user: User,
    mock_database: MagicMock,
) -> None:
    mock_database.get.return_value = sample_user
    cache = InMemoryCache(ttl_seconds=1)
    cache.set("users:1", sample_user)
    repo = UserRepository(cache=cache, database=mock_database)

    time.sleep(1.1)
    result = repo.get_by_id(1)

    assert result == sample_user
    mock_database.get.assert_called_once_with("users", 1)
    assert cache.get("users:1") == sample_user


def test_create_user_stores_in_cache(
    sample_user: User,
    mock_database: MagicMock,
) -> None:
    mock_database.create.return_value = sample_user
    cache = InMemoryCache(ttl_seconds=60)
    repo = UserRepository(cache=cache, database=mock_database)
    data = CreateUserRequest(name="Alice", email="alice@example.com", age=30)

    result = repo.create(data)

    assert result == sample_user
    assert cache.get("users:1") == sample_user


def test_update_user_stores_updated_user_in_cache(
    sample_user: User,
    mock_database: MagicMock,
) -> None:
    updated = User(id=1, name="Alice Updated", email="alice@example.com", age=31)
    mock_database.update.return_value = updated
    cache = InMemoryCache(ttl_seconds=60)
    repo = UserRepository(cache=cache, database=mock_database)
    data = UpdateUserRequest(name="Alice Updated", age=31)

    result = repo.update(user_id=1, data=data)

    assert result == updated
    assert cache.get("users:1") == updated


def test_get_all_returns_users_from_database(
    sample_user: User,
    mock_database: MagicMock,
) -> None:
    mock_database.get.return_value = [sample_user]
    cache = InMemoryCache(ttl_seconds=60)
    repo = UserRepository(cache=cache, database=mock_database)

    result = repo.get_all()

    assert result == [sample_user]
    mock_database.get.assert_called_once_with("users")
