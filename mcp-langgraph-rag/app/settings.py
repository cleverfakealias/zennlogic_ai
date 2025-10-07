from __future__ import annotations

"""Application settings and path helpers."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

load_dotenv()

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent
APP_ROOT: Final[Path] = PROJECT_ROOT
DATA_DIR_DEFAULT: Final[Path] = APP_ROOT / "data"
DOCS_DIR_DEFAULT: Final[Path] = DATA_DIR_DEFAULT / "docs"
INDEX_DIR_DEFAULT: Final[Path] = DATA_DIR_DEFAULT / "index"
NOTES_FILE_DEFAULT: Final[Path] = DATA_DIR_DEFAULT / "notes.txt"


class AppSettings(BaseModel):
    """Runtime configuration derived from environment variables."""

    model_config = ConfigDict(extra="ignore", frozen=True)

    openai_api_key: str | None = Field(default=None)
    chat_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-large")
    docs_dir: Path = Field(default_factory=lambda: DOCS_DIR_DEFAULT)
    index_dir: Path = Field(default_factory=lambda: INDEX_DIR_DEFAULT)
    notes_path: Path = Field(default_factory=lambda: NOTES_FILE_DEFAULT)

    @classmethod
    def from_env(cls) -> "AppSettings":
        """Instantiate settings from the current environment."""

        docs_dir_raw = os.getenv("DOCS_DIR")
        index_dir_raw = os.getenv("INDEX_DIR")
        notes_path_raw = os.getenv("NOTES_PATH")

        data: dict[str, object | None] = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "chat_model": os.getenv("CHAT_MODEL", "gpt-4o-mini"),
            "embedding_model": os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
        }

        if docs_dir_raw:
            data["docs_dir"] = Path(docs_dir_raw).expanduser()
        if index_dir_raw:
            data["index_dir"] = Path(index_dir_raw).expanduser()
        if notes_path_raw:
            data["notes_path"] = Path(notes_path_raw).expanduser()

        return cls(**data)

    def ensure_directories(self) -> None:
        """Create key directories if they do not yet exist."""

        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.notes_path.parent.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return a cached settings object."""

    settings = AppSettings.from_env()
    settings.ensure_directories()
    return settings


def reload_settings() -> AppSettings:
    """Reset the cached settings instance and return the new value."""

    get_settings.cache_clear()
    return get_settings()
