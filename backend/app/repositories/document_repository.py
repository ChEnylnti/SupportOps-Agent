from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.document import Document
from backend.app.schemas.document import DocumentCreate,DocumentUpdate,DocumentRead

def create_document(db: Session, document_in: DocumentCreate) -> Document:
    # document_in 是 Pydantic 的 DocumentCreate 对象。
    # model_dump() 会把它变成字典：
    # {
    # "filename": "...",
    # "doc_type": "...",
    # "description": "...",
    # "source_path": "..."
    # }
    document = Document(**document_in.model_dump())

    db.add(document)
    db.commit()
    # 从数据库重新读取这条记录，把数据库自动生成的字段拿回来
    db.refresh(document)

    return document

def get_document(db: Session, document_id:int) -> Document:
    statement = select(Document).where(Document.id == document_id)
    # db.scalar(...) 返回第一条结果，如果没有就返回 None。
    return db.scalar(statement)

def list_document(db:Session,skip: int = 0,limit:int=20) -> list[Document]:
    # 跳过前 skip 条 最多返回 limit 条 按 id 倒序，最新创建的排前面
    statement = select(Document).offset(skip).limit(limit).order_by(Document.id.desc())
    return list(db.scalars(statement).all())

def update_document(
        db: Session,
        document: Document,
        document_in: DocumentUpdate,
) -> Document:
    # exclude_unset=True 很重要。它的意思是：用户没传的字段不要出现在字典里。
    # 不会把 filename、doc_type 这些没传的字段覆盖成 None。
    update_data = document_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(document, field, value)

    db.add(document)
    db.commit()
    db.refresh(document)
    # 在 repository 层，update_document() 返回 Document 对象更合适；成功或失败应该交给 service / route 层处理
    return document

def delete_document(db: Session, document: Document) -> None:
    db.delete(document)
    db.commit()
    

