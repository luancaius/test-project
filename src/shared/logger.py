import structlog

from src.shared.settings import APP_TITLE

logger = structlog.get_logger(APP_TITLE)
