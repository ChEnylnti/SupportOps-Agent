from fastapi import FastAPI
from backend.app.core.config import get_settings
from backend.app.api.router import api_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )
    
    app.include_router(api_router, prefix=settings.api_prefix)
    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "SupportOps Agent API is running"}
    return app

app = create_app()