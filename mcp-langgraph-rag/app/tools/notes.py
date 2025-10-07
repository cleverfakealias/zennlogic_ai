from __future__ import annotations

"""Simple note-taking utilities used by the MCP server."""

from datetime import datetime, timezone

from app.settings import get_settings

_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def append_note(text: str) -> str:
    """Append a note with an ISO timestamp to the notes file."""

    settings = get_settings()
    settings.notes_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime(_TIMESTAMP_FORMAT)
    line = f"[{timestamp}] {text.strip()}\n"
    with settings.notes_path.open("a", encoding="utf-8") as handle:
        handle.write(line)
    return line


def read_notes(limit: int | None = None) -> list[str]:
    """Return recent note entries from the notes file."""

    settings = get_settings()
    if not settings.notes_path.exists():
        return []

    with settings.notes_path.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()

    if limit is None or limit >= len(lines):
        return [line.rstrip("\n") for line in lines]
    return [line.rstrip("\n") for line in lines[-limit:]]
