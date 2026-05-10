
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def create_test_document() -> dict:
    response = client.post(
        "/api/documents",
        json={
            "filename": "test_document.pdf",
            "doc_type": "faq",
            "description": "test description",
            "source_path": "/documents/test_document.pdf",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["code"] == 200
    assert body["message"] == "document created"

    return body["data"]


def test_create_document():
    document = create_test_document()

    assert document["id"] is not None
    assert document["filename"] == "test_document.pdf"
    assert document["doc_type"] == "faq"
    assert document["description"] == "test description"
    assert document["source_path"] == "/documents/test_document.pdf"
    assert document["chunk_count"] == 0
    assert "created_at" in document
    assert "updated_at" in document


def test_list_documents():
    created_document = create_test_document()

    response = client.get("/api/documents?skip=0&limit=20")

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == 200
    assert isinstance(body["data"], list)

    document_ids = [document["id"] for document in body["data"]]
    assert created_document["id"] in document_ids


def test_get_document():
    created_document = create_test_document()
    document_id = created_document["id"]

    response = client.get(f"/api/documents/{document_id}")

    assert response.status_code == 200

    body = response.json()
    document = body["data"]

    assert body["code"] == 200
    assert document["id"] == document_id
    assert document["filename"] == "test_document.pdf"


def test_update_document():
    created_document = create_test_document()
    document_id = created_document["id"]

    response = client.patch(
        f"/api/documents/{document_id}",
        json={
            "filename": "updated_document.pdf",
            "description": "updated description",
        },
    )

    assert response.status_code == 200

    body = response.json()
    document = body["data"]

    assert body["code"] == 200
    assert body["message"] == "document updated"
    assert document["id"] == document_id
    assert document["filename"] == "updated_document.pdf"
    assert document["description"] == "updated description"
    assert document["doc_type"] == "faq"


def test_delete_document():
    created_document = create_test_document()
    document_id = created_document["id"]

    response = client.delete(f"/api/documents/{document_id}")

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == 200
    assert body["message"] == "document deleted"

    get_response = client.get(f"/api/documents/{document_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Document not found"


def test_get_missing_document():
    response = client.get("/api/documents/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"