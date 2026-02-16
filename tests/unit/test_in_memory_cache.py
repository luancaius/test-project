"""Unit tests for InMemoryCache: get, set, and expired TTL behavior."""

import time

import pytest

from src.infra.cache.in_memory_cache import InMemoryCache


def test_get_missing_key_returns_none() -> None:
    cache = InMemoryCache(ttl_seconds=60)
    assert cache.get("missing") is None


def test_set_then_get_returns_value() -> None:
    cache = InMemoryCache(ttl_seconds=60)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_set_overwrites_existing_key() -> None:
    cache = InMemoryCache(ttl_seconds=60)
    cache.set("key1", "first")
    cache.set("key1", "second")
    assert cache.get("key1") == "second"


def test_different_keys_are_independent() -> None:
    cache = InMemoryCache(ttl_seconds=60)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_expired_entry_returns_none() -> None:
    """After TTL has passed, get returns None for the key."""
    cache = InMemoryCache(ttl_seconds=1)
    cache.set("expiring", "value")
    assert cache.get("expiring") == "value"
    time.sleep(1.1)
    assert cache.get("expiring") is None


def test_expired_entry_is_removed_from_store() -> None:
    """After TTL, get not only returns None but removes the entry (next get still None)."""
    cache = InMemoryCache(ttl_seconds=1)
    cache.set("expiring", "value")
    time.sleep(1.1)
    assert cache.get("expiring") is None
    assert cache.get("expiring") is None
    assert len(cache._store) == 0


def test_non_expired_entry_unchanged_after_other_expires() -> None:
    """One key expiring does not affect another key that has not expired."""
    cache = InMemoryCache(ttl_seconds=1)
    cache.set("short", "short_value")
    time.sleep(0.6)
    cache.set("long", "long_value")
    time.sleep(0.6)
    assert cache.get("short") is None
    assert cache.get("long") == "long_value"


def test_zero_ttl_expires_immediately() -> None:
    """With ttl_seconds=0, entry is considered expired on the next get (or very soon)."""
    cache = InMemoryCache(ttl_seconds=0)
    cache.set("zero", "v")
    time.sleep(0.1)
    assert cache.get("zero") is None
