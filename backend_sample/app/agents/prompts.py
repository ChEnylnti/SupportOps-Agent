from langchain_core.prompts import ChatPromptTemplate


# LangChain prompt templates keep LLM-facing text in one place. The current
# workflow uses this prompt only to build a preview; later we can pipe it into
# a chat model without changing the LangGraph topology.
REPLY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是 SupportOps Agent，负责基于企业知识库、风险判断和工单动作生成客服回复。",
        ),
        (
            "human",
            """
用户问题：
{user_message}

意图：{intent}
分类：{category}
风险等级：{risk_level}
缺失信息：{missing_fields}
知识库证据：{knowledge_summary}
工单信息：{ticket_summary}
审批信息：{approval_summary}

请生成一段简洁、专业、可执行的中文客服回复。
""",
        ),
    ]
)
