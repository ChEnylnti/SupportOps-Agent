from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_root() -> None:
    """The service root should prove the API process is running."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "SupportOps Agent API is running"}


def test_health_check() -> None:
    """The health endpoint should use the standard API envelope."""

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["data"]["status"] == "ok"


def test_chat_uses_supportops_graph() -> None:
    """A high-risk chat message should traverse approval and ticket nodes."""

    response = client.post("/api/chat", json={"message": "我想申请退款"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["intent"] == "refund_request"
    assert data["risk_level"] == "high"
    assert data["approval"]["status"] == "pending"
    assert data["ticket"]["status"] == "pending_approval"
    assert len(data["trace"]) == 7
