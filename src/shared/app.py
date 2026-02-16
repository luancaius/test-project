from fastapi import FastAPI
from starlette.requests import Request

from src.presentation.api.v1.router import router as v1_router
from src.shared.logger import logger
from src.shared.settings import settings


def get_fastapi_app() -> FastAPI:
    app = FastAPI(title=settings.app_title)

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        logger.info("request_started", method=request.method, path=request.url.path)
        response = await call_next(request)
        logger.info(
            "request_finished",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
        )
        return response

    @app.get("/")
    def root() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_title}

    app.include_router(v1_router)
    return app
