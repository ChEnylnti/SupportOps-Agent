from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.prompts import REPLY_PROMPT
from app.tools.approval_tools import request_human_approval
from app.tools.knowledge_tools import retrieve_knowledge
from app.tools.ticket_tools import create_ticket


class SupportOpsAgentState(TypedDict, total=False):
    """Shared state carried through the LangGraph workflow.

    Each node reads part of this state and returns only the fields it wants to
    add or update. LangGraph merges those partial updates into the next state.
    """

    user_message: str
    normalized_message: str
    intent: str
    category: str
    missing_fields: list[str]
    risk_level: str
    priority: str
    knowledge_results: list[dict[str, Any]]
    need_ticket: bool
    need_human_approval: bool
    ticket: dict[str, Any] | None
    approval: dict[str, Any] | None
    response: str
    prompt_preview: str
    trace: list[dict[str, Any]]


def _append_trace(
    state: SupportOpsAgentState, step: str, detail: dict[str, Any]
) -> list[dict[str, Any]]:
    """Append one workflow step to the trace without mutating the input state."""

    trace = list(state.get("trace", []))
    trace.append({"step": step, "detail": detail})
    return trace


def normalize_input(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Normalize user input before classification and retrieval."""

    message = state.get("user_message", "")
    normalized_message = " ".join(message.strip().split())

    return {
        "normalized_message": normalized_message,
        "trace": _append_trace(
            state,
            "normalize_input",
            {
                "normalized_message": normalized_message,
            },
        ),
    }


def classify_intent(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Classify intent, business category, risk level, and missing fields.

    This is deliberately rule-based for the first runnable version. Later this
    node can call an LLM through LangChain and return the same state fields.
    """

    message = state.get("normalized_message", state.get("user_message", ""))

    # The tuple shape is: keyword, intent, category, risk level, fields to ask.
    rules = [
        ("退款", "refund_request", "支付与退款", "high", ["订单号", "购买时间", "退款原因"]),
        ("权限", "permission_issue", "账号与权限", "high", ["系统名称", "目标角色", "直属主管"]),
        ("密码", "password_issue", "账号与权限", "medium", ["账号", "身份核验信息"]),
        ("登录", "login_issue", "账号与权限", "medium", ["系统名称", "报错截图"]),
        ("vpn", "vpn_issue", "网络与设备", "medium", ["操作系统", "错误码"]),
        ("VPN", "vpn_issue", "网络与设备", "medium", ["操作系统", "错误码"]),
        ("500", "system_error", "系统故障", "medium", ["发生时间", "访问路径", "错误截图"]),
        ("工单", "ticket_query", "工单流转", "low", ["工单编号"]),
    ]

    intent = "general_support"
    category = "通用咨询"
    risk_level = "low"
    missing_fields: list[str] = []

    for keyword, matched_intent, matched_category, matched_risk, fields in rules:
        if keyword in message:
            intent = matched_intent
            category = matched_category
            risk_level = matched_risk
            missing_fields = fields
            break

    return {
        "intent": intent,
        "category": category,
        "risk_level": risk_level,
        "missing_fields": missing_fields,
        "trace": _append_trace(
            state,
            "classify_intent",
            {
                "intent": intent,
                "category": category,
                "risk_level": risk_level,
                "missing_fields": missing_fields,
            },
        ),
    }


def retrieve_context(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Retrieve knowledge snippets that can support the final answer."""

    query = state.get("normalized_message", state.get("user_message", ""))
    category = state.get("category")
    results = retrieve_knowledge(query=query, category=category, top_k=3)

    return {
        "knowledge_results": results,
        "trace": _append_trace(
            state,
            "retrieve_context",
            {
                "result_count": len(results),
                "sources": [item["source"] for item in results],
            },
        ),
    }


def assess_risk(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Convert classification results into workflow decisions."""

    risk_level = state.get("risk_level", "low")
    category = state.get("category", "通用咨询")
    intent = state.get("intent", "general_support")

    priority_by_risk = {
        "high": "P1",
        "medium": "P2",
        "low": "P3",
    }
    priority = priority_by_risk.get(risk_level, "P3")
    need_human_approval = risk_level == "high"
    need_ticket = category != "通用咨询" and intent != "ticket_query"

    return {
        "priority": priority,
        "need_human_approval": need_human_approval,
        "need_ticket": need_ticket,
        "trace": _append_trace(
            state,
            "assess_risk",
            {
                "priority": priority,
                "need_human_approval": need_human_approval,
                "need_ticket": need_ticket,
            },
        ),
    }


def decide_next_step(
    state: SupportOpsAgentState,
) -> Literal["approval", "ticket", "reply"]:
    """Choose the next graph branch after risk assessment."""

    if state.get("need_human_approval"):
        return "approval"
    if state.get("need_ticket"):
        return "ticket"
    return "reply"


def create_approval_request(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Create a human approval request for high-risk operations."""

    approval = request_human_approval(
        action=f"处理{state.get('category', '通用咨询')}请求",
        risk_level=state.get("risk_level", "low"),
        reason="该问题可能涉及退款、权限变更或其他敏感操作。",
    )

    return {
        "approval": approval,
        "trace": _append_trace(
            state,
            "create_approval_request",
            {
                "approval_id": approval["approval_id"],
                "status": approval["status"],
            },
        ),
    }


def create_support_ticket(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Create a support ticket when the issue should enter operations flow."""

    ticket = create_ticket(
        title=state.get("normalized_message", state.get("user_message", ""))[:80],
        description=state.get("user_message", ""),
        category=state.get("category", "通用咨询"),
        priority=state.get("priority", "P3"),
        risk_level=state.get("risk_level", "low"),
    )

    return {
        "ticket": ticket,
        "trace": _append_trace(
            state,
            "create_support_ticket",
            {
                "ticket_id": ticket["ticket_id"],
                "department": ticket["department"],
                "status": ticket["status"],
            },
        ),
    }


def generate_reply(state: SupportOpsAgentState) -> SupportOpsAgentState:
    """Generate the user-facing response from all collected workflow context."""

    category = state.get("category", "通用咨询")
    risk_level = state.get("risk_level", "low")
    missing_fields = state.get("missing_fields", [])
    knowledge_results = state.get("knowledge_results", [])
    ticket = state.get("ticket")
    approval = state.get("approval")

    knowledge_summary = "；".join(
        f"{item['source']}：{item['content']}" for item in knowledge_results
    )
    ticket_summary = (
        f"{ticket['ticket_id']}，状态：{ticket['status']}，负责部门：{ticket['department']}"
        if ticket
        else "暂无工单"
    )
    approval_summary = (
        f"{approval['approval_id']}，状态：{approval['status']}" if approval else "无需审批"
    )

    prompt_value = REPLY_PROMPT.invoke(
        {
            "user_message": state.get("user_message", ""),
            "intent": state.get("intent", "general_support"),
            "category": category,
            "risk_level": risk_level,
            "missing_fields": "、".join(missing_fields) if missing_fields else "无",
            "knowledge_summary": knowledge_summary,
            "ticket_summary": ticket_summary,
            "approval_summary": approval_summary,
        }
    )
    prompt_preview = prompt_value.to_string()

    # The first version returns a deterministic reply. Later, this block can
    # call an LLM with `prompt_value` and keep the same output field: `response`.
    if risk_level == "high":
        response = (
            f"我已判断这是一个「{category}」问题，可能涉及敏感操作。"
            f"系统已创建人工确认请求：{approval['approval_id'] if approval else '待创建'}。"
            f"请补充：{'、'.join(missing_fields) if missing_fields else '必要证明材料'}。"
        )
    elif ticket:
        response = (
            f"我已判断这是一个「{category}」问题，并创建工单 {ticket['ticket_id']}，"
            f"当前状态为 {ticket['status']}，负责部门是 {ticket['department']}。"
            f"请补充：{'、'.join(missing_fields) if missing_fields else '更多上下文'}。"
        )
    else:
        response = (
            f"我已判断这是一个「{category}」问题。"
            "已基于当前知识库生成初步建议，如需人工处理可以继续补充问题细节。"
        )

    return {
        "response": response,
        "prompt_preview": prompt_preview,
        "trace": _append_trace(
            state,
            "generate_reply",
            {
                "response_preview": response,
                "used_langchain_prompt": True,
            },
        ),
    }


def build_supportops_graph():
    """Build and compile the SupportOps LangGraph workflow."""

    graph_builder = StateGraph(SupportOpsAgentState)

    # Nodes are small, composable steps. This makes each Agent decision visible
    # in trace logs and easier to test independently.
    graph_builder.add_node("normalize_input", normalize_input)
    graph_builder.add_node("classify_intent", classify_intent)
    graph_builder.add_node("retrieve_context", retrieve_context)
    graph_builder.add_node("assess_risk", assess_risk)
    graph_builder.add_node("create_approval_request", create_approval_request)
    graph_builder.add_node("create_support_ticket", create_support_ticket)
    graph_builder.add_node("generate_reply", generate_reply)

    graph_builder.add_edge(START, "normalize_input")
    graph_builder.add_edge("normalize_input", "classify_intent")
    graph_builder.add_edge("classify_intent", "retrieve_context")
    graph_builder.add_edge("retrieve_context", "assess_risk")
    # Conditional edges are where LangGraph starts to feel like an Agent
    # workflow instead of a plain chain: runtime state controls the next step.
    graph_builder.add_conditional_edges(
        "assess_risk",
        decide_next_step,
        {
            "approval": "create_approval_request",
            "ticket": "create_support_ticket",
            "reply": "generate_reply",
        },
    )
    graph_builder.add_edge("create_approval_request", "create_support_ticket")
    graph_builder.add_edge("create_support_ticket", "generate_reply")
    graph_builder.add_edge("generate_reply", END)

    return graph_builder.compile()


supportops_graph = build_supportops_graph()


def run_supportops_agent(user_message: str) -> SupportOpsAgentState:
    """Public entry point used by the FastAPI route."""

    initial_state: SupportOpsAgentState = {
        "user_message": user_message,
        "trace": [],
    }
    return supportops_graph.invoke(initial_state)
