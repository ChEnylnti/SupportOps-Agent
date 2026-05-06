from redis import Redis

from backend.app.core.config import get_settings

settings = get_settings()

redis_client = Redis.from_url(
    url= settings.redis_url,
    # 让 Redis 返回字符串，而不是 bytes
    decode_responses = True,
    # 连接 Redis 时，最多等 2 秒。
    socket_connect_timeout=2,
    # Redis 命令执行时，最多等 2 秒。
    socket_timeout=2,

)

def get_redis() -> Redis:
    return redis_client