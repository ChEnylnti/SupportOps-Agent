from fastapi import APIRouter,Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from redis import Redis
from redis.exceptions import RedisError
from fastapi.responses import JSONResponse
# from chromadb import HttpClient as Chromadb
from chromadb.api import ClientAPI

from backend.app.cache.redis import get_redis
from backend.app.core.config import get_settings
from backend.app.core.responses import success_response,error_response
from backend.app.db.session import get_db
from backend.app.vectorstores.chroma import get_chroma_client

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

@router.get("/health/db")
def database_health_check(db:Session = Depends(get_db)) -> dict[str, object]:
    """
    数据库健康检查接口。
    用最轻量的 SELECT 1 验证后端能否连上 PostgreSQL。
    """
    # 当前接口要用的数据库会话
    db.execute(text("SELECT 1"))
    return success_response(
        data={
            "database":"ok",
        }
    )

@router.get("/health/redis")
def redis_health_check(redis_client: Redis = Depends(get_redis)) -> dict[str, object]:
    try:
        redis_client.ping()
    except RecursionError as exc:
        return JSONResponse(
            status_code=503,
            content=error_response(
                message="Redis is unavailable",
                code=503,
                data={"detail": str(exc)},
            ),
        )
    return success_response(data={"redis":"ok"})
        
@router.get("/health/chroma")
def chroma_health_check(chroma_client: ClientAPI = Depends(get_chroma_client)) -> dict[str, object]:
    try:
        heartbeat = chroma_client.heartbeat()
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content=error_response(
                message="Chroma is unavaiblable",
                code=503,
                data={"detail": str(exc)},
            ),
        )
    return success_response(data={"chroma":"ok",
                                  "heartbeat": heartbeat,})