"""Document and metadata models for RAG pipeline."""

from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document with text and metadata."""

    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
