import time

import pytest

from src.business.models.user import User
from src.infra.cache.in_memory_user_cache import InMemoryUserCache


def test_get_user_missing_returns_none() -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    assert cache.get_user(1) is None


def test_set_user_then_get_user_returns_user(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_user(sample_user.id, sample_user)
    assert cache.get_user(sample_user.id) == sample_user


def test_set_user_overwrites_existing(
    sample_user: User,
    sample_user_2: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_user(1, sample_user)
    cache.set_user(1, sample_user_2)
    assert cache.get_user(1) == sample_user_2


def test_get_user_expired_returns_none_and_removes_entry(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=1)
    cache.set_user(sample_user.id, sample_user)
    assert cache.get_user(sample_user.id) == sample_user
    time.sleep(1.1)
    assert cache.get_user(sample_user.id) is None
    assert cache.get_user(sample_user.id) is None


def test_get_all_users_miss_returns_none() -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    assert cache.get_all_users() is None


def test_set_all_users_then_get_all_users_returns_list(
    sample_user: User,
    sample_user_2: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    users = [sample_user, sample_user_2]
    cache.set_all_users(users)
    result = cache.get_all_users()
    assert result is not None
    assert result == users


def test_get_all_users_returns_copy_not_internal_list(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_all_users([sample_user])
    result = cache.get_all_users()
    assert result is not None
    result.append(User(id=99, name="x", email="x@x.com", age=1))
    assert cache.get_all_users() == [sample_user]


def test_get_all_users_expired_returns_none_and_clears(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=1)
    cache.set_all_users([sample_user])
    assert cache.get_all_users() == [sample_user]
    time.sleep(1.1)
    assert cache.get_all_users() is None
    assert cache.get_all_users() is None


def test_invalidate_user_removes_one_user(
    sample_user: User,
    sample_user_2: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_user(1, sample_user)
    cache.set_user(2, sample_user_2)
    cache.invalidate_user(1)
    assert cache.get_user(1) is None
    assert cache.get_user(2) == sample_user_2


def test_invalidate_user_missing_id_is_no_op(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_user(sample_user.id, sample_user)
    cache.invalidate_user(999)
    assert cache.get_user(sample_user.id) == sample_user


def test_invalidate_all_clears_by_id_and_all(
    sample_user: User,
    sample_user_2: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_user(1, sample_user)
    cache.set_user(2, sample_user_2)
    cache.set_all_users([sample_user, sample_user_2])
    cache.invalidate_all()
    assert cache.get_user(1) is None
    assert cache.get_user(2) is None
    assert cache.get_all_users() is None


def test_zero_ttl_user_expires_immediately(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=0)
    cache.set_user(sample_user.id, sample_user)
    time.sleep(0.1)
    assert cache.get_user(sample_user.id) is None


def test_zero_ttl_all_expires_immediately(
    sample_user: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=0)
    cache.set_all_users([sample_user])
    time.sleep(0.1)
    assert cache.get_all_users() is None


def test_by_id_and_all_independent(
    sample_user: User,
    sample_user_2: User,
) -> None:
    cache = InMemoryUserCache(ttl_seconds=60)
    cache.set_user(1, sample_user)
    cache.set_all_users([sample_user_2])
    assert cache.get_user(1) == sample_user
    assert cache.get_all_users() == [sample_user_2]
    cache.invalidate_all()
    assert cache.get_user(1) is None
    assert cache.get_all_users() is None
