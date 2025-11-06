"""Chat endpoint for LLM."""

from typing import Any

from fastapi import APIRouter, Body
from pydantic import BaseModel

from service.config import settings
from service.llm.chains import LLMChain


router = APIRouter()
chain = LLMChain()


class ChatRequest(BaseModel):
    """Request model for the chat endpoint.

    messages: list of message dicts matching the LLM chat schema.
    model: optional model hint string.
    max_tokens: response token limit; defaults from settings.
    """

    messages: list[dict[str, Any]]
    model: str | None = None
    max_tokens: int = settings.max_tokens


# Module-level singleton for Body default
DEFAULT_BODY = Body(...)


@router.post("/", summary="Chat", description="Chat with LLM.")
async def chat(body: ChatRequest = DEFAULT_BODY) -> Any:
    """Chat with LLM."""
    return await chain.chat(body.messages, body.model, body.max_tokens)
