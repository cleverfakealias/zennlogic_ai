"""FastAPI app factory for zennlogic_ai_service REST API."""

from fastapi import Depends, FastAPI

from zennlogic_ai_service.auth.api_key import api_key_auth
from zennlogic_ai_service.rest.routers import chat, health, rag


app = FastAPI(title="zennlogic_ai_service", version="0.1.0")

app.include_router(health.router)
app.include_router(chat.router, prefix="/chat", dependencies=[Depends(api_key_auth)])
app.include_router(rag.router, prefix="/rag", dependencies=[Depends(api_key_auth)])
