"""App configuration loader for zennlogic_ai_service.

Reads environment variables and provides typed config.
"""

import os
from typing import Literal

from pydantic import BaseModel, Field


def _get_env_str(key: str, default: str) -> str:
    return os.getenv(key, default)


def _get_env_bool(key: str, default: str) -> bool:
    return os.getenv(key, default).lower() == "true"


def _get_env_int(key: str, default: str) -> int:
    return int(os.getenv(key, default))


def _get_vector_backend() -> Literal["faiss", "annoy", "auto"]:
    value = os.getenv("VECTOR_BACKEND", "auto")
    if value in ("faiss", "annoy", "auto"):
        return value  # type: ignore
    return "auto"


def _get_provider() -> Literal["openai", "bedrock"]:
    value = os.getenv("LLM_PROVIDER", "openai")
    if value in ("openai", "bedrock"):
        return value  # type: ignore
    return "openai"


def _get_embed_provider() -> Literal["openai", "bedrock"]:
    value = os.getenv("EMBED_PROVIDER", "openai")
    if value in ("openai", "bedrock"):
        return value  # type: ignore
    return "openai"


class Settings(BaseModel):
    """Application configuration settings."""

    # Environment
    env: str = Field(default_factory=lambda: _get_env_str("ENV", "local"))

    # AWS Configuration
    aws_region: str = Field(default_factory=lambda: _get_env_str("AWS_REGION", "us-east-1"))

    # API Keys
    openai_api_key: str | None = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))

    # AWS Services
    bedrock_region: str | None = Field(default_factory=lambda: os.getenv("BEDROCK_REGION"))
    ssm_api_key_param: str = Field(
        default_factory=lambda: f"/zennlogic/{os.getenv('ENV', 'local')}/api-key"
    )
    s3_bucket: str = Field(
        default_factory=lambda: f"zennlogic-{os.getenv('ENV', 'local')}-data-bucket"
    )
    s3_prefix: str = Field(default_factory=lambda: _get_env_str("S3_PREFIX", "faiss/"))

    # AI/ML Configuration
    vector_backend: Literal["faiss", "annoy", "auto"] = Field(default_factory=_get_vector_backend)
    embed_model: str = Field(
        default_factory=lambda: _get_env_str(
            "EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )
    )
    llm_provider: Literal["openai", "bedrock"] = Field(default_factory=_get_provider)
    embed_provider: Literal["openai", "bedrock"] = Field(default_factory=_get_embed_provider)

    # Tracing & Monitoring
    langsmith_tracing: bool = Field(
        default_factory=lambda: _get_env_bool("LANGSMITH_TRACING", "false")
    )

    # Model Parameters
    max_tokens: int = Field(default_factory=lambda: _get_env_int("MAX_TOKENS", "256"))
    top_k: int = Field(default_factory=lambda: _get_env_int("TOP_K", "5"))


settings = Settings()
