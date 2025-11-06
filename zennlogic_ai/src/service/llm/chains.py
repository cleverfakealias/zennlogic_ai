"""LLM chains for chat and RAG answer."""

from typing import Any


class LLMChain:
    """LLM chain for chat and embedding operations."""

    def __init__(self) -> None:
        """Initialize LLM chain with lazy provider instantiation."""
        from service.config import settings

        self.settings = settings
        # Cache created providers; avoid importing heavy deps unless selected.
        self._providers_cache: dict[str, Any] = {}

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> Any:
        """Chat with LLM and return the text response."""
        provider_key = self._select_provider(model)
        provider = self._get_provider(provider_key)
        return await provider.chat(messages, model=model, max_tokens=max_tokens)

    async def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> Any:
        """Generate embeddings for texts using the selected provider."""
        provider_key = self._select_provider(model)
        provider = self._get_provider(provider_key)
        return await provider.embed(texts, model=model)

    def _get_provider(self, key: str) -> Any:
        """Get or create the provider instance for the given key."""
        if key in self._providers_cache:
            return self._providers_cache[key]

        from service.llm.providers import AnthropicProvider, OpenAIProvider

        inst: Any
        if key == "openai":
            inst = OpenAIProvider(api_key=self.settings.openai_api_key)
        elif key == "anthropic":
            inst = AnthropicProvider(api_key=getattr(self.settings, "anthropic_api_key", None))
        elif key == "local":
            try:
                from service.llm.providers import LocalHFProvider

                inst = LocalHFProvider()
            except Exception as err:  # pragma: no cover - depends on optional deps
                raise RuntimeError("Local provider requires the 'transformers' package.") from err
        else:  # pragma: no cover - defensive coding
            raise ValueError(f"Unknown LLM provider: {key}")

        self._providers_cache[key] = inst
        return inst

    def _select_provider(self, model: str | None) -> str:
        """Select provider based on model hint or config default."""
        if model:
            m = model.lower()
            if "openai" in m or "gpt" in m:
                return "openai"
            if "anthropic" in m or "claude" in m:
                return "anthropic"
            if "local" in m or "hf" in m or "huggingface" in m:
                return "local"
        return self.settings.llm_provider
