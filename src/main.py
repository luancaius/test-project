import uvicorn
from src.shared.settings import settings
from src.shared.app import get_fastapi_app
from src.shared.di import init_dependencies

init_dependencies()
app = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.server_reload,
    )
