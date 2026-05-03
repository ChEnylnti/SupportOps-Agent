from fastapi import APIRouter

from app.core.config import settings
from app.core.responses import success_response

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Basic service health endpoint.

    Later phases will extend this with database, Redis, and Chroma checks.
    """

    return success_response(
        data={
            "status": "ok",
            "service": "supportops-agent",
            "version": settings.app_version,
            "environment": settings.app_env,
        }
    )
