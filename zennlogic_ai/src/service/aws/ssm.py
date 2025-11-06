"""SSM helpers for API key retrieval."""

from typing import Any


def get_ssm_client() -> Any:
    """Get configured SSM client.

    This is a placeholder used in tests and local development. Implement a
    real boto3.client('ssm') creation when wiring AWS credentials.
    """
    return None  # TODO: Implement actual client


def get_api_key() -> str | None:
    """Get API key from SSM parameter store.

    Returns the API key string when configured, otherwise None.
    """
    return None  # TODO: Implement actual key retrieval
