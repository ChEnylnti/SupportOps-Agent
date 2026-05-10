from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.core.responses import success_response
from backend.app.db.session import get_db 
from backend.app.schemas.document import DocumentCreate, DocumentRead,DocumentUpdate
from backend.app.services import document_service

router = APIRouter(prefix="/documents",tags=["documents"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_document(
    document_in: DocumentCreate,
    db:Session = Depends(get_db),
) -> dict[str, object]:
    document = document_service.create_document(db, document_in)
    
    return success_response(
        data=DocumentRead.model_validate(document).model_dump(mode="json"),
        message="document created",
    )

@router.get("")
def list_documents(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    documents = document_service.list_documents(db, skip=skip,limit=limit)

    return success_response(
        data=[
            DocumentRead.model_validate(document).model_dump(mode="json")
            for document in documents
        ]
    )

@router.get("/{document_id}")
def get_document(
    document_id:int,
    db:Session = Depends(get_db),
) -> dict[str,object]:
    document = document_service.get_document(db, document_id)
    return success_response(
        data=DocumentRead.model_validate(document).model_dump(mode="json")
    )
    
@router.patch("/{document_id}")
def update_document(
    document_id: int,
    document_in: DocumentUpdate,
    db:Session = Depends(get_db),
) -> dict[str, object]:
    document = document_service.update_document(db, document_id, document_in)
    return success_response(
        data=DocumentRead.model_validate(document).model_dump(mode="json"),
        message="document updated",
    )

@router.delete("/{document_id}")
def delete_document(
    document_id:int,
    db:Session = Depends(get_db),
)-> dict[str, object]:
    document_service.delete_document(db, document_id)
    
    return success_response(message="document deleted")