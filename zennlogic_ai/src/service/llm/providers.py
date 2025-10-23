"""LLM provider abstraction: OpenAI, Anthropic, and local HuggingFace."""

from typing import Any

import httpx
from structlog import get_logger


logger = get_logger()


class LLMProvider:
    """LLM provider abstraction base class."""

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> Any:
        """Chat with LLM provider.

        Args:
            messages: List of chat messages.
            model: Model/provider name.
            max_tokens: Max tokens for response.

        Raises:
            NotImplementedError: Always, must be implemented by subclass.
        """
        raise NotImplementedError()

    async def embed(self, texts: list[str], model: str | None = None) -> Any:
        """Generate embeddings via provider.

        Args:
            texts: List of texts.
            model: Model/provider name.

        Raises:
            NotImplementedError: Always, must be implemented by subclass.
        """
        raise NotImplementedError()

    """OpenAI chat provider using lowest-cost model (gpt-3.5-turbo)."""


class OpenAIProvider(LLMProvider):
    """OpenAI chat provider using lowest-cost model (gpt-3.5-turbo)."""

    def __init__(self, api_key: str | None) -> None:
        """Initialize OpenAIProvider.

        Args:
            api_key: OpenAI API key.
        """
        self.api_key = api_key
        self.model = "gpt-3.5-turbo"

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Chat with OpenAI model.

        Args:
            messages: List of chat messages.
            model: Model name.
            max_tokens: Max tokens for response.

        Returns:
            str: Model response.

        Raises:
            httpx.HTTPStatusError: If request fails.
        """
        mdl = model or self.model
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": mdl,
            "messages": messages,
            "max_tokens": max_tokens or 64,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            logger.info("openai.chat.success", model=mdl, tokens=max_tokens)
            return data["choices"][0]["message"]["content"]

    async def embed(self, texts: list[str], model: str | None = None):
        """Not implemented: OpenAI embedding."""
        raise NotImplementedError("OpenAI embedding not implemented.")

    """Anthropic chat provider using lowest-cost model (claude-3-haiku)."""


class AnthropicProvider(LLMProvider):
    """Anthropic chat provider using lowest-cost model (claude-3-haiku)."""

    def __init__(self, api_key: str | None):
        """Initialize AnthropicProvider.

        Args:
            api_key: Anthropic API key.
        """
        self.api_key = api_key
        self.model = "claude-3-haiku-20240307"

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
    ):
        """Chat with Anthropic model.

        Args:
            messages: List of chat messages.
            model: Model name.
            max_tokens: Max tokens for response.

        Returns:
            str: Model response.

        Raises:
            httpx.HTTPStatusError: If request fails.
        """
        mdl = model or self.model
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key or "",
            "Content-Type": "application/json",
        }
        prompt = self._format_prompt(messages)
        payload = {
            "model": mdl,
            "max_tokens": max_tokens or 64,
            "messages": messages,
            "prompt": prompt,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            logger.info("anthropic.chat.success", model=mdl, tokens=max_tokens)
            return data["content"]

    def _format_prompt(self, messages: list[dict[str, Any]]) -> str:
        """Format prompt for Anthropic API.

        Args:
            messages: List of chat messages.

        Returns:
            str: Concatenated prompt.
        """
        return "\n".join(m.get("content", "") for m in messages)

    async def embed(self, texts: list[str], model: str | None = None):
        """Not implemented: Anthropic embedding."""
        raise NotImplementedError("Anthropic embedding not implemented.")

    """Local HuggingFace provider (downloads/runs any model)."""


class LocalHFProvider(LLMProvider):
    """Local HuggingFace provider (downloads/runs any model)."""

    def __init__(self):
        """Initialize LocalHFProvider.

        Raises:
            RuntimeError: If transformers is not installed.
        """
        try:
            from transformers import pipeline
        except ImportError as err:
            raise RuntimeError("transformers not installed") from err
        self.pipeline = pipeline

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
    ):
        """Chat with local HuggingFace model.

        Args:
            messages: List of chat messages.
            model: Model name.
            max_tokens: Max tokens for response.

        Returns:
            str: Model response.
        """
        mdl = model or "gpt2"
        pipe = self.pipeline("text-generation", model=mdl)
        prompt = self._format_prompt(messages)
        result = pipe(prompt, max_new_tokens=max_tokens or 64)
        logger.info("localhf.chat.success", model=mdl, tokens=max_tokens)
        return result[0]["generated_text"]

    def _format_prompt(self, messages: list[dict[str, Any]]) -> str:
        """Format prompt for local HuggingFace model.

        Args:
            messages: List of chat messages.

        Returns:
            str: Concatenated prompt.
        """
        return "\n".join(m.get("content", "") for m in messages)

    async def embed(self, texts: list[str], model: str | None = None):
        """Not implemented: Local embedding."""
        raise NotImplementedError("Local embedding not implemented.")
