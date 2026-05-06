from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import get_settings

settings = get_settings()

# 数据库引擎： 负责和PostgreSQL建立连接
engine = create_engine(
    settings.database_url,
    # 先测试数据库连接还活不活,防止拿到一个已经失效的连接
    pool_pre_ping=True,
)

# Session工厂：后面每次请求都可以从这里那一个数据库绘画
SessionLocal = sessionmaker(
    # 不自动提交 事务要你自己控制
    autocommit=False,
    # 不自动把对象同步到数据库 更可控，适合项目开发
    autoflush=False,
    bind=engine,
    class_=Session,
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()