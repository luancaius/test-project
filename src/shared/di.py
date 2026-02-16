from typing import Optional

from src.business.services.user_service import UserService
from src.infra.cache.in_memory_cache import InMemoryCache
from src.infra.database.in_memory_user_database import InMemoryUserDatabase
from src.infra.repositories.user_repository import UserRepository
from src.shared.settings import CACHE_TTL_SECONDS


class Singletons:
    repository: Optional[UserRepository] = None
    user_service: Optional[UserService] = None


singletons = Singletons()


def init_dependencies() -> None:
    cache = InMemoryCache(ttl_seconds=CACHE_TTL_SECONDS)
    database = InMemoryUserDatabase()
    singletons.repository = UserRepository(cache=cache, database=database)
    singletons.user_service = UserService(repository=singletons.repository)
