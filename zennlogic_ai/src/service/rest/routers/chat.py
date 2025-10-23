"""Chat endpoint for LLM."""

from typing import Any

from fastapi import APIRouter, Body
from zennlogic_ai_service.config import settings
from zennlogic_ai_service.llm.chains import LLMChain


router = APIRouter()
chain = LLMChain()

# Module-level singleton for Body default
DEFAULT_BODY = Body(...)


@router.post("/", summary="Chat", description="Chat with LLM.")
def chat(
    messages: list[dict[str, Any]] = DEFAULT_BODY,
    model: str | None = None,
    max_tokens: int = settings.max_tokens,
) -> Any:
    """Chat with LLM."""
    return chain.chat(messages, model, max_tokens)
