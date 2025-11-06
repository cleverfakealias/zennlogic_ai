"""LLM chains for chat and RAG answer."""

from typing import Any


class LLMChain:
    """LLM chain for chat and embedding operations."""

    def __init__(self) -> None:
        """Initialize LLM chain with provider selection."""
        from service.config import settings
        from service.llm.providers import (
            AnthropicProvider,
            LocalHFProvider,
            OpenAIProvider,
        )

        self.settings = settings
        self.providers = {
            "openai": OpenAIProvider(api_key=settings.openai_api_key),
            "anthropic": AnthropicProvider(api_key=getattr(settings, "anthropic_api_key", None)),
            "local": LocalHFProvider(),
        }

    def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> Any:
        """Chat with LLM.

        Args:
            messages: List of chat messages.
            model: Model/provider name (str).
            max_tokens: Max tokens for response.

        Returns:
            str: Model response.
        """
        provider_key = self._select_provider(model)
        provider = self.providers[provider_key]
        return provider.chat(messages, model=model, max_tokens=max_tokens)

    def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> Any:
        """Generate embeddings for texts.

        Args:
            texts: List of texts.
            model: Model/provider name (str).

        Returns:
            Any: Embeddings.
        """
        provider_key = self._select_provider(model)
        provider = self.providers[provider_key]
        return provider.embed(texts, model=model)

    def _select_provider(self, model: str | None) -> str:
        """Select provider based on model string or config.

        Args:
            model: Model/provider name (str).

        Returns:
            str: Provider key ('openai', 'anthropic', 'local').
        """
        if model:
            m = model.lower()
            if "openai" in m or "gpt" in m:
                return "openai"
            if "anthropic" in m or "claude" in m:
                return "anthropic"
            if "local" in m or "hf" in m or "huggingface" in m:
                return "local"
        # fallback to config
        return self.settings.llm_provider
