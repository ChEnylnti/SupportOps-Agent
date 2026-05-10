from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.document import Document
from backend.app.repositories.document_repository import create_document as repo_create_document
from backend.app.repositories.document_repository import delete_document as repo_delete_document
from backend.app.repositories.document_repository import get_document as repo_get_document
from backend.app.repositories.document_repository import list_document as repo_list_document
from backend.app.repositories.document_repository import update_document as repo_update_document
from backend.app.schemas.document import DocumentCreate, DocumentUpdate

def create_document(db: Session, document_in: DocumentCreate)->Document:
    return repo_create_document(db, document_in)

def get_document(db: Session, document_id: int) -> Document:
    document = repo_get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

def list_documents(db:Session, skip:int =0, limit:int = 20) -> list[Document]:
    return repo_list_document(db, skip=skip, limit=limit)

def update_document(
        db: Session,
        document_id: int,

        document_in: DocumentUpdate,
)-> Document:
    document = repo_get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return repo_update_document(db, document, document_in)

def delete_document(db: Session, document_id: int) -> None:
    document = repo_get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    repo_delete_document(db, document)