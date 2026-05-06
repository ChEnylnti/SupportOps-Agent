from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "SupportOps Agent API is running"

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["message"] == "success"
    assert body["data"]["status"] == "ok"

def test_database_health():
    response = client.get("/api/health/db")
    assert response.status_code == 200

    body = response.json()
    assert body["code"] ==200
    assert body["message"] == "success"
    assert body["data"]["database"] == "ok"