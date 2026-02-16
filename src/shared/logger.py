from typing import Any

import structlog

from src.shared.settings import settings


class Logger:
    def __init__(self, name: str | None = None) -> None:
        self._logger = structlog.get_logger(name or settings.app_title)

    def info(self, event: str, **kwargs: Any) -> None:
        self._logger.info(event, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        self._logger.error(event, **kwargs)


logger = Logger()
