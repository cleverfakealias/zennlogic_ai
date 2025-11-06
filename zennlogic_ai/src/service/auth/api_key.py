"""API key auth dependency for FastAPI."""

from fastapi import Header, HTTPException, status

from service.aws.ssm import get_api_key
from service.config import settings


def api_key_auth(x_api_key: str | None = Header(None)) -> str:
    """Authenticate using API key from header.

    Returns the provided API key on success.
    """
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required")

    # In local development, use a test key; in other environments, fetch from SSM
    if settings.env == "local":
        expected: str | None = "test-api-key"  # Use a fixed test key for local development
    else:
        expected = get_api_key()

    if x_api_key != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return x_api_key
