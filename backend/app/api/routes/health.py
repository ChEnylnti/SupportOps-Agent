from fastapi import APIRouter

from backend.app.core.config import get_settings
from backend.app.core.responses import success_response

# 这个 router 专门放健康检查相关接口
router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check() -> dict[str, object]:
    """
    健康检查接口。
    用来确认后端服务是否正常运行。
    """
    settings = get_settings()

    return success_response(
        data={
            "status":"ok",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }
    )