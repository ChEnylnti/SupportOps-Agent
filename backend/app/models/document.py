from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base

class Document(Base):
    # 这张表在数据库里的名字
    __tablename__= "documents"
    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 文件名
    filename: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    # 文档类型，比如 faq、sop
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # 描述，可空
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 文件路径，可空
    source_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # 切分后的片段数
    chunk_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # 创建和更新时间
    created_at: Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        nullable=False,
        # 如果插入数据时你没有手动给 created_at，就让数据库服务器自动填当前时间。
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )