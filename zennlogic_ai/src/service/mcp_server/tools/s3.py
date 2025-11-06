"""MCP S3 tool: list objects."""

from typing import Any

from service.aws.s3 import get_s3_client
from service.config import settings


def list_objects(prefix: str) -> dict[str, list[str]]:
    """List S3 objects with prefix.

    Returns a mapping with the `objects` key containing the list of keys.
    """
    s3 = get_s3_client()
    resp: dict[str, Any] = s3.list_objects_v2(Bucket=settings.s3_bucket, Prefix=prefix)
    return {"objects": [obj["Key"] for obj in resp.get("Contents", [])]}
