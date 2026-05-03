from typing import Any


def success_response(data: Any = None, message: str = "success") -> dict[str, Any]:
    """Return the project's standard success envelope."""

    return {
        "code": 200,
        "message": message,
        "data": data if data is not None else {},
    }


def error_response(message: str, code: int = 400, data: Any = None) -> dict[str, Any]:
    """Return the project's standard error envelope."""

    return {
        "code": code,
        "message": message,
        "data": data,
    }
