from datetime import UTC, datetime
from uuid import uuid4


def request_human_approval(
    action: str,
    risk_level: str,
    reason: str,
) -> dict:
    """Create a mock human approval request for sensitive actions."""

    return {
        "approval_id": f"APR-{uuid4().hex[:8].upper()}",
        "action": action,
        "risk_level": risk_level,
        "reason": reason,
        "status": "pending",
        "created_at": datetime.now(UTC).isoformat(),
    }
