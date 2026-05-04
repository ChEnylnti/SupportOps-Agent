"""应用配置集中管理。

这个文件的职责只有一个：把项目里会变化的参数统一收起来。
例如应用名、环境、数据库地址、Redis 地址、模型名称等。
这样后面业务代码就不用到处写死常量了。
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """项目配置模型。

    BaseSettings 的特点是：
    1. 会自动从环境变量读取同名配置；
    2. 也可以从 .env 文件读取；
    3. 字段上写的默认值，会在没配置环境变量时生效。
    """

    # 这段配置告诉 Pydantic：去哪里找环境变量文件，以及遇到额外字段时怎么处理。
    model_config = SettingsConfigDict(
        env_file=".env",          # 根目录下的 .env 文件
        env_file_encoding="utf-8",  # 使用 UTF-8 读取，避免中文乱码
        extra="ignore",           # .env 里多出来的字段先忽略，不报错
    )

    # ===== 应用基础信息 =====
    # 这些内容一般用于接口文档、日志和前端展示。
    app_name: str = "SupportOps Agent"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api"

    # ===== 基础设施连接信息 =====
    # database_url 是数据库连接串。
    # 这里先写默认值，后面可以在 .env 中覆盖。
    database_url: str = Field(
        default="postgresql+psycopg://supportops:supportops@localhost:5432/supportops"
    )

    # Redis 用于缓存、任务状态、临时会话状态等。
    redis_url: str = "redis://localhost:6379/0"

    # Chroma 向量库的地址和端口。
    chroma_host: str = "localhost"
    chroma_port: int = 8001

    # ===== AI 模型相关配置 =====
    # str | None 表示“要么是字符串，要么是空值”。
    # 这样即使暂时没有填 API Key，项目也能先启动。
    ai_api_key: str | None = None
    chat_model: str | None = None
    embedding_model: str | None = None


@lru_cache
def get_settings() -> Settings:
    """获取配置对象。

    lru_cache 的作用是缓存结果。
    也就是说，第一次调用时创建 Settings 对象，
    后面再次调用时直接复用，不会重复读取配置。
    """

    return Settings()
