from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Shared API response schema used for documentation and future typing."""

    code: int = 200
    message: str = "success"
    data: Any = {}
