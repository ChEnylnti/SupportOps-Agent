from fastapi import APIRouter

from app.agents.supportops_graph import run_supportops_agent
from app.core.responses import success_response
from app.schemas.chat import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest) -> dict:
    """Run the SupportOps LangGraph workflow for one user message."""

    result = run_supportops_agent(request.message)

    # Keep the API response explicit so the frontend can render each workflow
    # artifact independently: answer, classification, ticket, approval, trace.
    return success_response(
        data={
            "message": result.get("response", ""),
            "intent": result.get("intent"),
            "category": result.get("category"),
            "risk_level": result.get("risk_level"),
            "priority": result.get("priority"),
            "missing_fields": result.get("missing_fields", []),
            "knowledge_results": result.get("knowledge_results", []),
            "ticket": result.get("ticket"),
            "approval": result.get("approval"),
            "trace": result.get("trace", []),
        }
    )
