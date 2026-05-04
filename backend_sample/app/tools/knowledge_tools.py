# Temporary in-memory knowledge source.
#
# In the production path this module will call Chroma/pgvector after documents
# have been chunked and embedded. Keeping the tool function shape now lets the
# LangGraph node stay stable when storage changes later.
KNOWLEDGE_SNIPPETS = [
    {
        "source": "FAQ.md",
        "category": "账号与权限",
        "content": "登录失败时需要确认账号是否激活、密码是否正确、系统权限是否开通，并提供系统名称和报错截图。",
    },
    {
        "source": "SOP.md",
        "category": "账号与权限",
        "content": "权限申请需要提交系统名称、目标角色、申请原因和直属主管审批信息。",
    },
    {
        "source": "RefundPolicy.md",
        "category": "支付与退款",
        "content": "退款申请需要核实订单号、购买时间、退款原因，并在需要时进入财务或人工审批流程。",
    },
    {
        "source": "ITHelpdeskGuide.md",
        "category": "网络与设备",
        "content": "VPN 无法连接时需要检查外网、客户端版本、账号权限和证书状态。",
    },
    {
        "source": "FAQ.md",
        "category": "系统故障",
        "content": "系统 500 错误需要记录发生时间、访问路径、操作步骤和错误截图，并交由研发或运维排查。",
    },
]


def retrieve_knowledge(query: str, category: str | None = None, top_k: int = 3) -> list[dict]:
    """Return mock RAG results for a query and optional category."""

    normalized_query = query.lower()
    scored_results = []

    for snippet in KNOWLEDGE_SNIPPETS:
        score = 0
        if category and snippet["category"] == category:
            score += 2
        # Simple keyword scoring keeps the first version deterministic and easy
        # to understand before we introduce embeddings and vector similarity.
        for token in ["登录", "权限", "退款", "vpn", "VPN", "500", "故障", "订单"]:
            if token.lower() in normalized_query and token in snippet["content"]:
                score += 1
        if score > 0:
            scored_results.append({**snippet, "score": score})

    if not scored_results:
        scored_results = [{**item, "score": 0} for item in KNOWLEDGE_SNIPPETS[:1]]

    return sorted(scored_results, key=lambda item: item["score"], reverse=True)[:top_k]
