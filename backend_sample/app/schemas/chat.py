from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for one chat turn.

    `conversation_id` is optional for now; it will become useful when we add
    persistent conversation history.
    """

    message: str = Field(..., min_length=1, description="用户输入的问题")
    conversation_id: str | None = Field(default=None, description="会话 ID")
