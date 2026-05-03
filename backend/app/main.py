from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    """Create the FastAPI application and wire global infrastructure.

    Keeping app creation inside a function makes testing easier: tests can build a
    fresh app instance without importing a process-wide server.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    # Global concerns are registered once at startup, before business routes.
    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "SupportOps Agent API is running"}

    return app


# Uvicorn imports this variable when running `uvicorn app.main:app`.
app = create_app()
