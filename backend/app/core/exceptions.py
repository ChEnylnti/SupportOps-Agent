from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.responses import error_response


class AppError(Exception):
    """Business-level exception that can be safely returned to API clients."""

    def __init__(self, message: str, code: int = 400) -> None:
        self.message = message
        self.code = code


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for consistent API error responses."""

    @app.exception_handler(AppError)
    async def app_error_handler(
        request: Request, exc: AppError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.code,
            content=error_response(message=exc.message, code=exc.code),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # FastAPI raises this when request body/query/path validation fails.
        return JSONResponse(
            status_code=422,
            content=error_response(message="请求参数校验失败", code=422),
        )
