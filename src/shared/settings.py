import os


class Settings:
    def __init__(self) -> None:
        self.log_level: str = os.environ.get("LOG_LEVEL", "INFO")
        self.cache_ttl_seconds: int = int(os.environ.get("CACHE_TTL_SECONDS", "60"))
        self.server_host: str = os.environ.get("SERVER_HOST", "0.0.0.0")
        self.server_port: int = int(os.environ.get("SERVER_PORT", "8000"))
        self.server_reload: bool = bool(os.environ.get("SERVER_RELOAD", "true"))
        self.app_title: str = os.environ.get("APP_TITLE", "User Service")


settings = Settings()
