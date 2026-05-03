from datetime import UTC, datetime
from uuid import uuid4


# First-version routing rules. Later these will move into database-backed
# configuration so operations teams can change ownership without code deploys.
DEPARTMENT_BY_CATEGORY = {
    "账号与权限": "IT支持组",
    "网络与设备": "网络组",
    "支付与退款": "财务组",
    "系统故障": "研发支持组",
    "工单流转": "客服组",
    "通用咨询": "客服组",
}


def create_ticket(
    title: str,
    description: str,
    category: str,
    priority: str,
    risk_level: str,
) -> dict:
    """Create a mock ticket payload.

    This is shaped like a future database record, so callers do not need to know
    whether the ticket is currently in memory or persisted in PostgreSQL.
    """

    return {
        "ticket_id": f"TCK-{uuid4().hex[:8].upper()}",
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "risk_level": risk_level,
        "department": DEPARTMENT_BY_CATEGORY.get(category, "客服组"),
        "status": "pending_approval" if risk_level == "high" else "new",
        "created_at": datetime.now(UTC).isoformat(),
    }
