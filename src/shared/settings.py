import os

LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
CACHE_TTL_SECONDS: int = int(os.environ.get("CACHE_TTL_SECONDS", "60"))
SERVER_HOST: str = os.environ.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT: int = int(os.environ.get("SERVER_PORT", "8000"))
SERVER_RELOAD: bool = bool(os.environ.get("SERVER_RELOAD", "true"))
APP_TITLE: str = os.environ.get("APP_TITLE", "User Service")
