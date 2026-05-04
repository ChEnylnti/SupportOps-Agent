from fastapi import APIRouter

from app.api.routes import chat, health


# Central API router. Feature routers are registered here, while `main.py`
# attaches the shared `/api` prefix from settings.
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, tags=["chat"])
