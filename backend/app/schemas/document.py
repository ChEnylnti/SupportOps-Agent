from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# 这个类不是普通类，而是一个“数据校验模型”。FastAPI 会用它自动检查请求体是否合法
# DocumentCreate   创建文档时，前端需要传什么
class DocumentCreate(BaseModel):
    # Field(...) 是字段规则
    filename: str = Field(min_length=1, max_length=255)
    doc_type: str = Field(min_length=1, max_length=50)
    description: str | None = None
    source_path: str | None = None

# 修改文档时，前端可以传什么
class DocumentUpdate(BaseModel):
    filename: str | None = Field(default=None, min_length=1, max_length=255)
    doc_type: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    source_path: str | None = None

# 后端返回给前端什么
class DocumentRead(BaseModel):
    # 允许 Pydantic 从 SQLAlchemy 模型对象里读取字段。
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    doc_type: str
    description: str | None
    source_path: str | None
    chunk_count: int
    created_at: datetime
    updated_at: datetime