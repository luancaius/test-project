import uvicorn
from src.shared.settings import SERVER_HOST, SERVER_PORT, SERVER_RELOAD
from src.shared.app import get_fastapi_app
from src.shared.di import init_dependencies

init_dependencies()
app = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_RELOAD,
    )
