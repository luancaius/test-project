
from src.business.services.user_service import UserService
from src.infra.cache.in_memory_cache import InMemoryCache
from src.infra.database.in_memory_user_database import InMemoryUserDatabase
from src.infra.repositories.user_repository import UserRepository
from src.shared.settings import settings


class Singletons:
    repository: UserRepository | None = None
    user_service: UserService | None = None


singletons = Singletons()


def init_dependencies() -> None:
    cache = InMemoryCache(ttl_seconds=settings.cache_ttl_seconds)
    database = InMemoryUserDatabase()
    singletons.repository = UserRepository(cache=cache, database=database)
    singletons.user_service = UserService(repository=singletons.repository)
