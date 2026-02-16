import time
from typing import Any

from src.infra.cache.cache import Cache


class InMemoryCache(Cache):
    """In-memory cache with TTL. Entries expire after ttl_seconds."""

    def __init__(self, ttl_seconds: int = 60) -> None:
        self._ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, at = entry
        if time.time() > at + self._ttl_seconds:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (value, time.time())
