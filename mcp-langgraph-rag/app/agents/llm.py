from __future__ import annotations

"""Factories for language model clients used by the agent graph."""

from typing import Final

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.settings import get_settings

_DEFAULT_TEMPERATURE: Final[float] = 0.0
_DEFAULT_TIMEOUT: Final[int] = 30
_MAX_RETRIES: Final[int] = 2


def get_chat_model(*, temperature: float = _DEFAULT_TEMPERATURE) -> BaseChatModel:
    """Instantiate a chat model driven by environment configuration."""

    settings = get_settings()
    client = ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.chat_model,
        temperature=temperature,
        timeout=_DEFAULT_TIMEOUT,
        max_retries=_MAX_RETRIES,
    )
    return client
